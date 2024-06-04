from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from .forms import CustomUserCreationForm, UserProfilForm
from .models import Course, Enrollment, Grade
from .forms import GradeForm  # Formulaire à créer pour ajouter des notes

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
    success_url = reverse_lazy('users:password_change_done')

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

# Vues pour la gestion des cours et des notes

@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'notes/course_list.html'
    context_object_name = 'courses'

@method_decorator(login_required, name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    template_name = 'notes/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['enrollments'] = Enrollment.objects.filter(course=course)
        return context

@method_decorator(login_required, name='dispatch')
class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'notes/add_grade.html'

    def form_valid(self, form):
        form.instance.enrollment = get_object_or_404(Enrollment, pk=self.kwargs['enrollment_id'])
        return super().form_valid(form)

    def get_success_url(self):
        enrollment = self.object.enrollment
        return reverse_lazy('course_detail', kwargs={'pk': enrollment.course.id})

@method_decorator(login_required, name='dispatch')
class GradeUpdateView(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'notes/edit_grade.html'

    def get_success_url(self):
        enrollment = self.object.enrollment
        return reverse_lazy('course_detail', kwargs={'pk': enrollment.course.id})
s