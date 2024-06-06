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
from .forms import (CustomAuthenticationForm, CustomUserCreationForm,
                    UserProfileForm)
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import *


class UserCreationView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

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
    success_url = reverse_lazy('administration:dashboard')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            kwargs['instance'] = user
        else:
            kwargs['instance'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            context['profile_user'] = user
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
def attendance_teacher(request):
    user = request.user
    
    
    sessions = Session.objects.order_by('-date')
    
    maintenant = timezone.now()


    sessions = [session for session in sessions if session.date <= maintenant]
  
    
    context = {'user': user, 'sessions':sessions}

    return render(request,'attendance/attendance_teacher.html',context)

def attendance_student(request):
    user = request.user
    
    absences = Presence.objects.filter(user=user,presence="Absent")
    lates = Presence.objects.filter(user=user,presence="Late", justified = False)
    
  
    
    context = {'user': user,'absences':absences, 'lates':lates}

    return render(request,'attendance/attendance_student.html',context)

def attendance_admin(request):
    
    if request.method == 'POST':
         username= request.POST['student']
         return HttpResponseRedirect('/attendance_of/%s/'% username)
    

    return render(request,'attendance/attendance_admin.html')

def attendance_of(request,username):
    user=get_object_or_404(CustomUser,username=username)
    presence = Presence.objects.filter(user=user).exclude(presence="Present")
    presence=presence.order_by('-session__date')
    
    if request.method == 'POST':
        print("test")
        for p in presence:
            
            justified_value = request.POST.get(str(p.pk), 'off')
            p.justified = (justified_value == "on")
            p.save()
        return HttpResponseRedirect("/attendance_admin/")

    
    
    
    


    context ={'user':user, 'presence':presence}
    return render(request,'attendance/attendance_of.html',context)


def class_call(request, id):
    user = request.user
    
    
    session = get_object_or_404(Session, pk=id)
    lesson= session.lesson
    group=lesson.group

    student_list = group.users.order_by('last_name')
    
    if request.method == 'POST':
        for student in student_list:
            attendance_status = request.POST.get(student.username)
            attendance, created = Presence.objects.get_or_create(
                user=student,
                session=session,
                Room=session.room 

            )
            attendance.presence = attendance_status
            attendance.save()
            session.is_called_done = True
            session.save()
        return HttpResponseRedirect("/attendance_teacher/")
        
        
    
    context = {'user': user, 'session':session, 'student_list':student_list}

    return render(request,'attendance/class_call.html',context)


 
