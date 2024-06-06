from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render, redirect
from .models import Subject, Grade, UE, Group, Lesson

@login_required
def studentview(request):
    user = request.user
    user_promo= Group.objects.filter(type="promo",users=user).first()
    ues_average=[]
    subj_average=[]
    teachers=[]
    i=0
    if (user.user_type == 'student'):
        if user_promo is not None:
            subj_average = [[] for _ in range(user_promo.ues.count())]
            teachers = [[] for _ in range(user_promo.ues.count())]
            for ue in user_promo.ues.all() :
                ave = 0.0
                sum=0
                for s in ue.Subjects.all():
                    ave_s=0.0
                    sum_coeff_s=0
                    lesson = Lesson.objects.filter(subject=s).first()
                    if lesson:
                        teacher = lesson.teacher
                        teachers[i].append(teacher.last_name)
                    else : 
                        teachers[i].append("-")
                    for g in Grade.objects.filter(subject=s,user=user):
                        ave_s+=g.grade*g.coeff
                        sum_coeff_s+=g.coeff
                    ave_s/=sum_coeff_s
                    ave+=ave_s*s.coeff
                    sum+=s.coeff
                    subj_average[i].append(round(ave_s,2))
                i+=1
                ave/=sum
                ues_average.append(round(ave,2))
        context = {'user': user, 'user_promo':user_promo, 'ues_average':ues_average, 'subj_average':subj_average, 'teachers':teachers}
    else :
        context = {'user': user}
    return render(request,'notes/studentview.html',context)

@login_required
def profview(request):
    user = request.user
    lessons = Lesson.objects.filter(teacher=user)
    subjects = [lesson.subject for lesson in lessons]
    groups=Group.objects.filter(type="promo")
    context = {'user': user,'subjects':subjects,'groups':groups}

    return render(request,'notes/profview.html',context)

@login_required
def profview_entergrades(request):
    user = request.user
    if request.method == "POST":
        subject = request.POST.get('subject')
        group = request.POST.get('class')
        coefficient = request.POST.get('coefficient')
        group=Group.objects.filter(name=group).first()
        students = group.users.filter(user_type='student').order_by('last_name')
        context = {
            'user':user,
            'subject': subject,
            'group': group,
            'coefficient': coefficient,
            'students':students,
        }

        return render(request, 'notes/entergrades.html', context)
    else:
        return render(request, 'notes/entergrades.html')

@login_required
def profview_grades(request):
    user = request.user

    if request.method == "POST":
        subject = request.POST.get('subject')
        group = request.POST.get('group')
        coefficient = request.POST.get('coefficient')
        group=Group.objects.filter(name=group).first()
        students = group.users.filter(user_type='student').order_by('last_name')

        grades = []
        for student in students:
            grade = request.POST.get(str(student.id))
            grades.append(grade)

        context = {
            'user':user,
            'subject': subject,
            'group': group,
            'coefficient': coefficient,
            'students':students,
            'grades': grades,
        }

        return render(request, 'notes/profviewgrades.html', context)
    else:
        return render(request, 'notes/profviewgrades.html')

class UserCreationView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        if (self.object.user_type == 'student' or
                self.object.user_type == 'teacher'):
            return reverse_lazy('user_portal:dashboard')
        elif self.object.user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == 'student' or user.user_type == 'teacher':
                return reverse(
                    'user_portal:dashboard')
            elif user.user_type == 'admin':
                return reverse(
                    'administration:dashboard')


class CustomLogoutView(LogoutView):
    next_page = 'users:login'


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')  # reverse_lazy
    # permet de convertir le chemin relatif en url, nécessaire ici pour
    # success_url.


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


class ProfileView(FormView):
    template_name = "users/profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy('main:home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
