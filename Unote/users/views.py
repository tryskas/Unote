from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from .forms import CustomUserCreationForm, UserProfilForm
from django.shortcuts import render, redirect
from .models import Subject, Grade, UE, Group


def studentview(request):
    user = request.user
    user_promo= Group.objects.filter(type="promo",users=user).first()
    ues_average=[]
    subj_average = [[] for _ in range(user_promo.ues.count())]
    i=0
    for ue in user_promo.ues.all() :
        ave = 0.0
        sum=0
        for s in ue.Subjects.all():
            ave_s=0.0
            sum_coeff_s=0
            for g in Grade.objects.filter(Subject=s,user=user):
                ave_s+=g.grade*g.coeff
                sum_coeff_s+=g.coeff
            ave_s/=sum_coeff_s
            ave+=ave_s*s.coeff
            sum+=s.coeff
            subj_average[i].append(ave_s)
        i+=1
        ave/=sum
        ues_average.append(ave)
        

    context = {'user': user, 'user_promo':user_promo, 'ues_average':ues_average, 'subj_average':subj_average}

    return render(request,'notes/studentview.html',context)


class UserCreationView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    next_page = 'main:home'


class CustomLogoutView(LogoutView):
    next_page = 'main:home'


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


class ProfilView(FormView):
    template_name = "users/profil.html"
    form_class = UserProfilForm
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
