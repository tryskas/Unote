from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from users.models import CustomUser
from administration.models import Subject, UE
from .forms import SubjectForm, UEForm
from django.contrib import messages
from django.http import HttpResponseRedirect


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "administration/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == 'admin':
            return redirect('main:error_403')
        return super().dispatch(request, *args, **kwargs)


@login_required
def profiles(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    context = {}

    return render(request, 'administration/profiles.html', context)


@login_required
@require_GET
def search_user(request):
    search_term = request.GET.get('search_term', '')

    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    users = CustomUser.objects.filter(Q(first_name__icontains=search_term) |
                                      Q(last_name__icontains=search_term) |
                                      Q(username__icontains=search_term))

    search_results_html = render_to_string(
        'administration/search_user_results.html',
        {'search_results': users})

    return JsonResponse({'search_user_results_html':
                         search_results_html})


@login_required
def groups(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    context = {}

    return render(request, 'administration/groups.html', context)


@login_required
def courses(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    context = {}

    return render(request, 'administration/courses.html', context)


@login_required
def absences(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    context = {}

    return render(request, 'administration/absences.html', context)


@login_required
def eus(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    ues = UE.objects.all()

    context = {'ues': ues}

    return render(request, 'administration/eus.html', context)


@login_required
@require_GET
def search_ue(request):
    search_term = request.GET.get('search_term', '')

    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    ues = UE.objects.filter(Q(name__icontains=search_term))

    search_results_html = render_to_string(
        'administration/search_ue_results.html',
        {'search_results': ues})

    return JsonResponse({'search_ue_results_html':
                         search_results_html})


class UECreationView(CreateView):
    template_name = 'administration/ue_creation.html'
    form_class = UEForm

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


class UEUpdateView(UpdateView):
    model = UE
    template_name = 'administration/update_ue.html'
    form_class = UEForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ue = self.get_object()
        context['ue'] = ue
        return context

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


@login_required
@require_POST
def delete_ue(request, ue_id):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    try:
        ue = UE.objects.get(pk=ue_id)
        ue.delete()
        messages.success(request, 'L\'UE a été supprimée avec succès.')
    except UE.DoesNotExist:
        messages.error(request, 'L\'UE n\'existe pas.')

    return redirect('administration:dashboard')


@login_required
def subjects(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    subjects = Subject.objects.all()

    context = {'subjects': subjects}

    return render(request, 'administration/subjects.html',
                  context)


@login_required
@require_GET
def search_subject(request):
    search_term = request.GET.get('search_term', '')

    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    subjects = Subject.objects.filter(Q(name__icontains=search_term))

    search_results_html = render_to_string(
        'administration/search_subject_results.html',
        {'search_results': subjects})

    return JsonResponse({'search_subject_results_html':
                         search_results_html})


class SubjectCreationView(CreateView):
    template_name = 'administration/subject_creation.html'
    form_class = SubjectForm

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'administration/update_subject.html'
    form_class = SubjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        context['subject'] = subject
        return context

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


@login_required
@require_POST
def delete_subject(request, subject_id):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    try:
        subject = Subject.objects.get(pk=subject_id)
        subject.delete()
        messages.success(request, 'La matière a été supprimée avec succès.')
    except Subject.DoesNotExist:
        messages.error(request, 'La matière n\'existe pas.')

    return redirect('administration:dashboard')
