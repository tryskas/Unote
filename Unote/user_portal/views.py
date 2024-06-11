from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from administration.models import (Subject, Grade, UE, Group, Presence,
                                   Session, Course)
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from datetime import timedelta , datetime
import locale


class DashboardView(TemplateView):
    template_name = "user_portal/dashboard.html"


class MyAccountView(TemplateView):
    template_name = "user_portal/my_account.html"


@login_required
def studentview(request):
    user = request.user
    user_promo = Group.objects.filter(type="promo", users=user).first()
    ues_average = []
    subj_average = []
    teachers = []
    subj_list = []
    no_note = True
    ues_list = []

    i = 0
    if user.user_type == 'student':
        if user_promo is not None:

            for unite in user_promo.ues.all():
                subj = unite.subjects.all()
                for j in range(len(subj)):
                    if (Grade.objects.filter(subject=subj[j],
                                             user=user) and unite not in ues_list):
                        ues_list.append(unite)
            print(ues_list)
            subj_list = [[] for _ in range(len(ues_list))]
            subj_average = [[] for _ in range(len(ues_list))]
            teachers = [[] for _ in range(len(ues_list))]
            for ue in ues_list:
                ave = 0.0
                sum = 0

                for subj in ue.subjects.all():
                    if Grade.objects.filter(subject=subj, user=user):
                        subj_list[i].append(subj)
                print(subj_list)
                print(ues_list)
                if subj_list[i]:
                    no_note = False
                    for s in subj_list[i]:
                        ave_s = 0.0
                        sum_coeff_s = 0
                        course = Course.objects.filter(subject=s).first()
                        if course:
                            teacher = course.teacher
                            teachers[i].append(teacher.last_name)
                        else:
                            teachers[i].append("-")
                        for g in Grade.objects.filter(subject=s, user=user):
                            ave_s += g.grade * g.coeff
                            sum_coeff_s += g.coeff
                        ave_s /= sum_coeff_s
                        ave += ave_s * s.coeff
                        sum += s.coeff
                        subj_average[i].append(round(ave_s, 2))
                    i += 1
                    ave /= sum
                    ues_average.append(round(ave, 2))
        context = {
            'user': user,
            'user_promo': user_promo,
            'ues_average': ues_average,
            'subj_average': subj_average,
            'teachers': teachers,
            'subj_list': subj_list,
            'ues_list': ues_list,
            'no_note': no_note
        }

    else:
        context = {'user': user}
    return render(request, 'user_portal/studentview.html', context)


@login_required
def profview(request):
    user = request.user
    courses = Course.objects.filter(teacher=user)
    subjects = [course.subject for course in courses]
    groups= []
    for l in courses:
        for g in Group.objects.filter(type="promo"):
            if l.group==g:
                groups.append(g)
    print(groups)
    context = {'user': user,'subjects':subjects,'groups':groups}

    return render(request,'user_portal/profview.html',context)


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

        return render(request, 'user_portal/entergrades.html', context)
    else:
        return render(request, 'user_portal/entergrades.html')


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

        return render(request, 'user_portal/successgrades.html', context)
    else:
        return render(request, 'user_portal/successgrades.html')


@login_required
def profview_grades(request):
    user = request.user

    if request.method == "POST":
        group = request.POST.get('group')
        group = Group.objects.filter(name=group).first()
        students = group.users.filter(user_type='student').order_by('last_name')

        for student in students:
            grade_value = request.POST.get(str(student.id))
            if grade_value is not None:
                grade = Grade.objects.create(
                    grade=grade_value,
                    coeff=request.POST.get('coefficient'),
                    user=student,
                    subject=Subject.objects.filter(name=request.POST.get(
                        'subject')).first()
                )
                grade.save()
        context = {
            'user':user,
            'group': group,
        }

        return render(request, 'user_portal/profview.html', context)
    else:
        return render(request, 'user_portal/profviewgrades.html')


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


def weekly_schedule(request):
    user = request.user
    today = timezone.now()
    today=today.replace(hour= 7)
    if user.user_type == 'student' :
        group=Group.objects.filter(users=user).all()
        course=Course.objects.filter(group__in = group).all()
    else :
        course=Course.objects.filter(teacher=user).all()



    print(today)
     
    if request.method == "POST":
        start = request.POST.get('start_of_week')
        start = start.strip()
        direction = request.POST.get('week')
        format = "%d %B %Y %H:%M"
        
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        startofweek = datetime.strptime(start, format)
         
        startofweek = timezone.make_aware(startofweek) 
        locale.setlocale(locale.LC_TIME, 'en_EN.UTF-8')
        
        if direction == "past_week":
            startofweek -= timedelta(days=7)
        elif direction == "next_week":
            startofweek += timedelta(days=7)
        
        start_of_week = startofweek
    else:
        start_of_week = today - timedelta(days=today.weekday())

    day_mapping = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        'Sunday': 'Dimanche'
        }
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    hours = range(8, 21)
    week_dates = [(start_of_week + timedelta(days=i)).strftime('%d/%m') for i in range(7)]
    day_date_mapping = dict(zip(days, week_dates))
    
    start_of_week=start_of_week.replace(hour= 7)
    
    
    
       
    end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week
    end_of_week=end_of_week.replace(hour= 22)
    print (start_of_week)
    print (end_of_week)
    print([start_of_week, end_of_week])
    sessions = Session.objects.filter(date__range=[start_of_week, end_of_week],course__in = course).order_by('date')
    print( sessions )
   

    timetable = {day: {hour: None for hour in hours} for day in days}
    
   
    
    for session in sessions:
            session_date = timezone.localtime(session.date)
            day_name = session_date.strftime('%A')
            day_name_fr = day_mapping[day_name]
            hour = session_date.hour
            
            total_seconds = session.duration.total_seconds()

        
            total_hours = int(total_seconds / 3600)
            if 8 <= hour < 21:
                for i in range(0,total_hours):
                
                    timetable[day_name_fr][hour+i] = session
                
                
    

    context = {
            'timetable': timetable,
            'hours': hours,
            'days': days,
            'day_date_mapping' : day_date_mapping,
            'start_of_week' : start_of_week
        }
   
    
    
    return render(request, 'schedule/schedule.html', context)
