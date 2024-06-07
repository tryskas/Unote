from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from administration.models import Subject, Grade, UE, Group, Presence,Session
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse


class DashboardView(TemplateView):
    template_name = "user_portal/dashboard.html"


def student_view(request):
    user = request.user
    ues = UE.objects.all()
    subjects = Subject.objects.all()
    grades = Grade.objects.all()
    user_promo = Group.objects.filter(type="promo", users=user).first()

    context = {'user': user, 'subjects': subjects, 'grades': grades,
               'ues': ues, 'user_promo': user_promo}
    return render(request, 'user_portal/student_view.html', context)


def attendance_student(request):
    user = request.user
    absences = Presence.objects.filter(user=user, presence="absent",
                                       justified=False)
    lates = Presence.objects.filter(user=user, presence="late",
                                    justified=False)

    context = {'user': user, 'absences': absences, 'lates': lates}

    return render(request, 'attendance/attendance_student.html', context)


def attendance_teacher(request):
    user = request.user
    sessions = Session.objects.order_by('-date')
    now = timezone.now()
    sessions = [session for session in sessions if session.date <= now]
    context = {'user': user, 'sessions': sessions}

    return render(request, 'attendance/attendance_teacher.html', context)


def class_call(request, id):
    user = request.user

    session = get_object_or_404(Session, pk=id)
    course = session.course
    group = course.group

    student_list = group.users.order_by('last_name')

    if request.method == 'POST':
        for student in student_list:
            attendance_status = request.POST.get(student.username)
            attendance, created = Presence.objects.get_or_create(
                user=student,
                session=session
            )
            attendance.presence = attendance_status
            attendance.save()
            session.is_called_done = True
            session.save()
        return HttpResponseRedirect(reverse("user_portal:attendance_teacher"))

    context = {'user': user, 'session': session, 'student_list': student_list}

    return render(request, 'attendance/class_call.html', context)
