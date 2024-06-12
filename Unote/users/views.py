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
                    UserProfileForm, CSVUploadForm)
from django.shortcuts import get_object_or_404, redirect, render
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import csv
from django.contrib import messages
from django.views.decorators.http import require_POST


def send_password_email(email, username, password):
    subject = 'Unote - Vos identifiants de connexion'
    message = f"""
    Bonjour,

    Vos identifiants pour le site "Unote" ont été créés. Vous trouverez ci-dessous vos informations de connexion :

    Identifiant : {username}
    Mot de passe : {password}

    Nous vous recommandons de changer votre mot de passe dès votre première connexion pour des raisons de sécurité. Voici les étapes pour accéder au site et modifier votre mot de passe :

    1. Rendez-vous sur https://unote.alwaysdata.net.
    2. Connectez-vous avec les identifiants fournis ci-dessus.
    3. Allez dans la section "Mon Compte".
    4. Suivez les instructions pour changer votre mot de passe.

    Si vous rencontrez des problèmes pour vous connecter ou si vous avez des questions, n'hésitez pas à contacter notre support à unoteservice@gmail.com.

    Nous vous remercions et vous souhaitons une excellente utilisation de la plateforme "Unote".

    Cordialement,

    L'équipe Unote
    """
    recipient_list = [email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
              recipient_list)


@method_decorator(login_required, name='dispatch')
class UserCreationView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user, password = form.save()
        send_password_email(user.email, user.username, password)
        messages.success(self.request, 'L\'utilisateur a bien été créé.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == 'admin':
            return redirect('main:error_403')
        return super().dispatch(request, *args, **kwargs)


@login_required
def upload_csv(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            users_created = 0
            for row in reader:
                form = CustomUserCreationForm({
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'user_type': row['user_type']
                })
                if form.is_valid():
                    user, password = form.save()
                    send_password_email(user.email, user.username, password)
                    users_created += 1
                else:
                    messages.error(request, f"Erreur lors de l'enregistrement de l'utilisateur {row['email']}")
            messages.success(request, f"{users_created} utilisateurs ont été créés avec succès.")
            return redirect(reverse_lazy('users:register'))
    else:
        form = CSVUploadForm()
    return render(request, 'users/upload_csv.html', {'form': form})


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


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')  # reverse_lazy
    # permet de convertir le chemin relatif en url, nécessaire ici pour
    # success_url.


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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
        messages.success(self.request, 'Profil mis à jour.')
        form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == 'admin':
            return redirect('main:error_403')
        return super().dispatch(request, *args, **kwargs)


@login_required
@require_POST
def delete_user(request, user_id):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    user_to_delete = CustomUser.objects.get(pk=user_id)
    user_to_delete.delete()
    messages.success(request, 'L\'utilisateur a été supprimé.')

    return redirect('administration:dashboard')


@login_required
def delete_csv(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            users_deleted = 0
            for row in reader:
                try:
                    user = CustomUser.objects.get(
                        email=row['email'],
                        first_name=row['first_name'],
                        last_name=row['last_name']
                    )
                    user.delete()
                    users_deleted += 1
                except Exception as e:
                    messages.error(request, f"Erreur lors de la suppression de l'utilisateur avec l'email {row['email']}: {str(e)}")
            messages.success(request, f"{users_deleted} utilisateurs ont été supprimés avec succès.")
            return redirect(reverse_lazy('administration:dashboard'))
    else:
        form = CSVUploadForm()
    return render(request, 'users/delete_csv.html', {'form': form})
