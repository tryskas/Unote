from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from administration.models import Subject, Grade, UE, Group, Presence,Session
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from administration.models import *

class DashboardView(TemplateView):
    template_name = "user_portal/dashboard.html"


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
                subj = unite.subjects.all()
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
                
                for subj in ue.subjects.all():
                   if (Grade.objects.filter(subject=subj,user=user)):
                        subj_list[i].append(subj)
                print(subj_list)
                print(ues_list)
                if (subj_list[i]):
                    no_note = False
                    for s in subj_list[i]:
                        ave_s=0.0
                        sum_coeff_s=0
                        course = Course.objects.filter(subject=s).first()
                        if course:
                            teacher = course.teacher
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
    return render(request,'user_portal/studentview.html',context)

@login_required
def profview(request):
    user = request.user
    courses = Course.objects.filter(teacher=user)
    subjects = [course.subject for course in courses]
    groups= []
    for l in courses:
        for g in Group.objects.filter(type="promo"):
            if (l.group==g):
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

        return render(request, 'user_portal/profview.html', context)
    else:
        return render(request, 'user_portal/profviewgrades.html')

def attendance_student(request):
    user = request.user
    absences = Presence.objects.filter(user=user, presence="Absent")
    lates = Presence.objects.filter(user=user, presence="Late",
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
