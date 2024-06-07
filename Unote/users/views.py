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
