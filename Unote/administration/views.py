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
from .forms import SubjectForm, UEForm, GroupForm, CourseForm, RoomForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from administration.models import *


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

    groups = Group.objects.all()

    context = {'groups': groups}

    return render(request, 'administration/groups.html', context)


@login_required
@require_GET
def search_group(request):
    search_term = request.GET.get('search_term', '')

    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    groups = Group.objects.filter(Q(name__icontains=search_term))

    search_results_html = render_to_string(
        'administration/search_group_results.html',
        {'search_results': groups})

    return JsonResponse({'search_group_results_html':
                         search_results_html})


class GroupCreationView(CreateView):
    template_name = 'administration/group_creation.html'
    form_class = GroupForm

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'administration/update_group.html'
    form_class = GroupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()
        context['group'] = group
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
def delete_group(request, group_id):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    try:
        group = Group.objects.get(pk=group_id)
        group.delete()
        messages.success(request, 'La matière a été supprimée avec succès.')
    except Group.DoesNotExist:
        messages.error(request, 'La matière n\'existe pas.')

    return redirect('administration:dashboard')


@login_required
def courses(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    courses = Course.objects.all()

    context = {'courses': courses}

    return render(request, 'administration/courses.html', context)


@login_required
@require_GET
def search_course(request):
    search_term = request.GET.get('search_term', '')

    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    courses = Course.objects.filter(Q(name__icontains=search_term))

    search_results_html = render_to_string(
        'administration/search_course_results.html',
        {'search_results': courses})

    return JsonResponse({'search_course_results_html':
                         search_results_html})


class CourseCreationView(CreateView):
    template_name = 'administration/course_creation.html'
    form_class = CourseForm

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'administration/update_course.html'
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['course'] = course
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
def delete_course(request, course_id):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    try:
        course = Course.objects.get(pk=course_id)
        course.delete()
        messages.success(request, 'Le cours a été supprimée avec succès.')
    except Course.DoesNotExist:
        messages.error(request, 'Le cours n\'existe pas.')

    return redirect('administration:dashboard')


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


@login_required
def rooms(request):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    rooms = Room.objects.all()

    context = {'rooms': rooms}

    return render(request, 'administration/rooms.html',
                  context)


@login_required
@require_GET
def search_room(request):
    search_term = request.GET.get('search_term', '')

    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    rooms = Room.objects.filter(Q(name__icontains=search_term))

    search_results_html = render_to_string(
        'administration/search_room_results.html',
        {'search_results': rooms})

    return JsonResponse({'search_room_results_html':
                         search_results_html})


class RoomCreationView(CreateView):
    template_name = 'administration/room_creation.html'
    form_class = RoomForm

    def get_success_url(self):
        user_type = self.request.user.user_type
        if user_type == 'student' or user_type == 'teacher':
            return reverse_lazy('user_portal:dashboard')
        elif user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'administration/update_room.html'
    form_class = RoomForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        context['room'] = room
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
def delete_room(request, room_id):
    if request.user.user_type != "admin":
        return render(request, 'main/403.html', status=403)

    try:
        room = Room.objects.get(pk=room_id)
        room.delete()
        messages.success(request, 'La salle a été supprimée avec succès.')
    except Room.DoesNotExist:
        messages.error(request, 'La salle n\'existe pas.')

    return redirect('administration:dashboard')


def attendance_of(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    presence = Presence.objects.filter(user=user).exclude(presence="present")
    presence = presence.order_by('-session__date')

    if request.method == 'POST':
        for p in presence:
            justified_value = request.POST.get(str(p.pk), 'off')
            p.justified = (justified_value == "on")
            p.save()

        return HttpResponseRedirect(reverse("users:profile", args=[user.id]))

    context = {'user': user, 'presence': presence}
    return render(request, 'administration/attendance_of.html', context)
