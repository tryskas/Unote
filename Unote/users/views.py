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
from .models import Subject, Grade, UE, Group, Lesson
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def studentview(request):
    user = request.user
    user_promo= Group.objects.filter(type="promo",users=user).first()
    ues_average=[]
    subj_average=[]
    teachers=[]
    subj_list =[]
    no_note=True
    ues_list=[]

    i=0
    if (user.user_type == 'student'):
        if user_promo is not None:
            
            for unite in user_promo.ues.all():
                subj = unite.Subjects.all()
                for j in range(len(subj)):    
                    if (Grade.objects.filter(subject=subj[j],user=user) and unite not in ues_list):
                        ues_list.append(unite)
            print(ues_list)
            subj_list = [[] for _ in range(len(ues_list))]
            subj_average = [[] for _ in range(len(ues_list))]
            teachers = [[] for _ in range(len(ues_list))]
            for ue in  ues_list:
                ave = 0.0
                sum=0
                
                for subj in ue.Subjects.all():
                   if (Grade.objects.filter(subject=subj,user=user)):
                        subj_list[i].append(subj)
                print(subj_list)
                print(ues_list)
                if (subj_list[i]):
                    no_note = False
                    for s in subj_list[i]:
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
        context = {
            'user': user, 
            'user_promo':user_promo, 
            'ues_average':ues_average, 
            'subj_average':subj_average, 
            'teachers':teachers,
            'subj_list':subj_list,
            'ues_list':ues_list,
            'no_note':no_note
        }
        
    else :
        context = {'user': user}
    return render(request,'notes/studentview.html',context)

@login_required
def profview(request):
    user = request.user
    lessons = Lesson.objects.filter(teacher=user)
    subjects = [lesson.subject for lesson in lessons]
    groups= []
    allsubj = Subject.objects.all()
    allgroups = Group.objects.filter(type="promo").all()
    for l in lessons:
        for g in Group.objects.filter(type="promo"):
            if (l.group==g):
                groups.append(g)
    print(groups)
    context = {
        'user': user,
        'subjects':subjects,
        'groups':groups,
        'allsubj':allsubj,
        'allgroups':allgroups
        }

    
    return render(request,'notes/profview.html',context)

@login_required
def profviewhome(request):
    user = request.user
    context = {
        'user':user,
    }
    return render(request,'notes/profviewhome.html',context)


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
def success_grades(request):
    user = request.user

    if request.method == "POST":
        group = request.POST.get('group')
        group=Group.objects.filter(name=group).first()
        students = group.users.filter(user_type='student').order_by('last_name')

        for student in students:
            grade_value = request.POST.get(str(student.id))
            if grade_value is not None:
                grade = Grade.objects.create(
                    grade=grade_value,
                    coeff=request.POST.get('coefficient'),
                    user=student,
                    subject=Subject.objects.filter(name=request.POST.get('subject')).first()
                )
                grade.save()
        context = {
            'user':user,
            'group': group,
        }

        return render(request, 'notes/successgrades.html', context)
    else:
        return render(request, 'notes/successgrades.html')

def profview_grades(request):
    user = request.user
    groups = Group.objects.filter(type="promo").all()
    subjects = Subject.objects.all()
    no_grades=True
    context = {
            'user':user,
            'groups': groups,
            'subjects':subjects,
            'no_grades':no_grades
    }
    if request.method == "POST":
        group = Group.objects.filter(name=request.POST.get('group')).first()
        students = group.users.filter(user_type='student').order_by('last_name')
        subject =Subject.objects.filter(name=request.POST.get('subj')).first()
        grades=[[] for _ in range(len(students))]
        
        for i,student in enumerate(students):
            for g in Grade.objects.filter(subject=subject,user=student):
                no_grades=False    
                grades[i].append(g)

        max_grades = max(len(student_grades) for student_grades in grades)
        
        #Remplir les endroits vides du tableau
        for student_grades in grades:
            while len(student_grades) < max_grades:
                student_grades.append(None)
        grade_range = range(max_grades)
        stud_ave=[[] for _ in range(len(students))]
        class_ave=[[] for _ in range(max_grades)]
        if (no_grades==False):
            #Calcul des moyennes de chaque eleves et de chaque notes
            for i,s in enumerate(students):
                stu_ave=0
                coeff_stu_ave=0
                for g in grades[i]:
                    if g:
                        stu_ave+=g.grade*g.coeff
                        coeff_stu_ave+=g.coeff
                if (coeff_stu_ave!=0):
                    stud_ave[i]=round(stu_ave/coeff_stu_ave,2)
                else :
                    stud_ave[i]=" "
            
            for i in range(max_grades):
                tot_stud=len(students)
                clas_ave=0
                for j in range(tot_stud):
                    if (grades[j][i]):
                        clas_ave+=grades[j][i].grade
                    else :
                        tot_stud-=1
                class_ave[i]=round(clas_ave/tot_stud,2)
            print(class_ave)
            print(tot_stud)
        context = {
            'user':user,
            'group':group,
            'subject':subject,
            'groups': groups,
            'subjects':subjects,
            'students':students,
            'grades':grades,
            'grade_range':grade_range,
            'no_grades':no_grades,
            'stud_ave':stud_ave,
            'class_ave':class_ave
        }
        

        return render(request, 'notes/profviewgrades.html', context)
    else:
        return render(request, 'notes/profviewgrades.html',context)

@login_required
def delete_selected_grades(request):
    if request.method == 'POST':
        grades_to_delete = request.POST.getlist('grades_to_delete')
        if grades_to_delete:
            Grade.objects.filter(pk__in=grades_to_delete).delete()
        return redirect('users:modify_grades')
    return redirect('users:modify_grades')


#afficher les notes avec moy etc
@login_required
def modify_grades(request):
    user = request.user
    groups = Group.objects.filter(type="promo").all()
    subjects = Subject.objects.all()
    no_grades=True
    context = {
            'user':user,
            'groups': groups,
            'subjects':subjects,
            'no_grades':no_grades
    }
    if request.method == "POST":
        group = Group.objects.filter(name=request.POST.get('group')).first()
        students = group.users.filter(user_type='student').order_by('last_name')
        subject =Subject.objects.filter(name=request.POST.get('subj')).first()
        grades=[[] for _ in range(len(students))]
        
        for i,student in enumerate(students):
            for g in Grade.objects.filter(subject=subject,user=student):
                no_grades=False    
                grades[i].append(g)

        max_grades = max(len(student_grades) for student_grades in grades)
        
        #Remplir les endroits vides du tableau
        for student_grades in grades:
            while len(student_grades) < max_grades:
                student_grades.append(None)
        grade_range = range(max_grades)
        stud_ave=[[] for _ in range(len(students))]
        class_ave=[[] for _ in range(max_grades)]
        if (no_grades==False):
            #Calcul des moyennes de chaque eleves et de chaque notes
            for i,s in enumerate(students):
                stu_ave=0
                coeff_stu_ave=0
                for g in grades[i]:
                    if g:
                        stu_ave+=g.grade*g.coeff
                        coeff_stu_ave+=g.coeff
                if (coeff_stu_ave!=0):
                    stud_ave[i]=round(stu_ave/coeff_stu_ave,2)
                else :
                    stud_ave[i]=" "
            
            for i in range(max_grades):
                tot_stud=len(students)
                clas_ave=0
                for j in range(tot_stud):
                    if (grades[j][i]):
                        clas_ave+=grades[j][i].grade
                    else :
                        tot_stud-=1
                class_ave[i]=round(clas_ave/tot_stud,2)
            print(class_ave)
            print(tot_stud)
        context = {
            'user':user,
            'group':group,
            'subject':subject,
            'groups': groups,
            'subjects':subjects,
            'students':students,
            'grades':grades,
            'grade_range':grade_range,
            'no_grades':no_grades,
            'stud_ave':stud_ave,
            'class_ave':class_ave
        }
        

        return render(request, 'notes/modifygrades.html', context)
    else:
        return render(request, 'notes/modifygrades.html',context)




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
