from django.template.loader import render_to_string
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from administration.models import (Subject, Grade, UE, Group, Presence,
                                   Session, Course)
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from django.db.models import Q, F, ExpressionWrapper,DateTimeField

from users.models import CustomUser


def dashboard_view(request):
    user = request.user
    absence_late = Presence.objects.filter(user=user, justified=False).exclude(presence="present").order_by('-session__date')[:3]
    grades = Grade.objects.filter(user=user)[:3]
    user_groups = Group.objects.filter(users=user)
    future_exams = Session.objects.filter( date__gt=timezone.now(), exam=True, course__group__in=user_groups).distinct().order_by('date')[:3]

    context = { 'user': user, 'absence_late': absence_late, 'grades': grades, 'future_exams': future_exams }

    return render(request, 'user_portal/dashboard.html', context)


class MyAccountView(TemplateView):
    template_name = "user_portal/my_account.html"


@login_required
def studentview(request):
    user = request.user

    if user.user_type != 'student':
        return render(request, 'user_portal/studentview.html', {'user': user})

    user_promo = get_user_promo(user)
    if not user_promo:
        return render(request, 'user_portal/studentview.html', {'user': user})

    ues_list = get_ues_list(user, user_promo)
    subj_list, subj_average, teachers, ues_average, no_note = get_subjects_and_averages(user, ues_list)

    context = {
        'user': user,
        'user_promo': user_promo,
        'ues_average': ues_average,
        'subj_average': subj_average,
        'teachers': teachers,
        'subj_list': subj_list,
        'ues_list': ues_list,
        'no_note': no_note,
    }

    return render(request, 'user_portal/studentview.html', context)


@login_required
def profviewhome(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request,'user_portal/profviewhome.html',context)


@login_required
def profview(request):
    user = request.user
    courses = Course.objects.filter(teacher=user)
    subjects = [course.subject for course in courses]

    groups = list({course.group for course in courses if course.group.type == "promo"})

    all_subjects = Subject.objects.all()
    all_groups = Group.objects.filter(type="promo")

    context = {
        'user': user,
        'subjects': subjects,
        'groups': groups,
        'allsubj': all_subjects,
        'allgroups': all_groups,
    }

    return render(request, 'user_portal/profview.html', context)


@login_required
def profview_entergrades(request):
    user = request.user
    if request.method == "POST":
        subject = request.POST.get('subject')
        group_name = request.POST.get('class')
        coefficient = request.POST.get('coefficient')

        group=Group.objects.filter(name=group_name).first()
        if group:
            students = group.users.filter(user_type='student').order_by('last_name')
        else:
            students = []

        context = {
            'user':user,
            'subject': subject,
            'group': group,
            'coefficient': coefficient,
            'students':students,
        }

        return render(request, 'notes/entergrades.html', context)
    else:
        return render(request, 'notes/entergrades.html')


@login_required
def success_grades(request):
    user = request.user

    if request.method == "POST":
        group_name = request.POST.get('group')
        subject_name = request.POST.get('subject')
        coefficient = request.POST.get('coefficient')

        group = get_object_or_404(Group, name=group_name)
        subject = get_object_or_404(Subject, name=subject_name)

        students = group.users.filter(user_type='student').order_by(
            'last_name')

        for student in students:
            grade_value = request.POST.get(str(student.id))
            if grade_value:
                grade = Grade.objects.create(
                    grade=grade_value,
                    coeff=coefficient,
                    user=student,
                    subject=subject
                )
                grade.save()
        context = {
            'user': user,
            'group': group,
        }
        return render(request, 'notes/successgrades.html', context)

    return render(request, 'notes/successgrades.html')


@login_required
def profview_grades(request):
    user = request.user
    all_groups = Group.objects.filter(type="promo").all()
    all_subjects = Subject.objects.all()

    courses = Course.objects.filter(teacher=user)
    subjects = [course.subject for course in courses]
    groups = list(
        {course.group for course in courses if course.group.type == "promo"})

    no_grades = True
    context = {
        'user': user,
        'all_groups': all_groups,
        'all_subjects': all_subjects,
        'groups': groups,
        'subjects': subjects,
        'no_grades': no_grades,
    }

    if request.method == "POST":
        group, subject = get_group_and_subject(request)
        students, grades, no_grades, max_grades = get_students_and_grades(group, subject)
        grade_range = range(max_grades)

        if not no_grades:
            stud_ave, class_ave = calculate_averages(students, grades, max_grades)
        else:
            stud_ave = []
            class_ave = []

        context.update({
            'all_groups': all_groups,
            'all_subjects': all_subjects,
            'group': group,
            'subject': subject,
            'students': students,
            'grades': grades,
            'grade_range': grade_range,
            'no_grades': no_grades,
            'stud_ave': stud_ave,
            'class_ave': class_ave,
        })

    return render(request, 'notes/profviewgrades.html', context)


@login_required
def delete_selected_grades(request):
    if request.method == 'POST':
        grades_to_delete = request.POST.getlist('grades_to_delete')
        if grades_to_delete:
            Grade.objects.filter(pk__in=grades_to_delete).delete()
        return redirect('user_portal:modify_grades')
    return redirect('user_portal:modify_grades')


@login_required
def modify_grades(request):
    user = request.user
    all_groups = Group.objects.filter(type="promo").all()
    all_subjects = Subject.objects.all()

    courses = Course.objects.filter(teacher=user)
    subjects = [course.subject for course in courses]
    groups = list(
        {course.group for course in courses if course.group.type == "promo"})

    no_grades = True
    context = {
        'user': user,
        'all_groups': all_groups,
        'all_subjects': all_subjects,
        'groups': groups,
        'subjects': subjects,
        'no_grades': no_grades,
    }

    if request.method == "POST":
        group, subject = get_group_and_subject(request)
        students, grades, no_grades, max_grades = get_students_and_grades(
            group, subject)
        grade_range = range(max_grades)

        if not no_grades:
            stud_ave, class_ave = calculate_averages(students, grades,
                                                     max_grades)
        else:
            stud_ave = []
            class_ave = []

        context.update({
            'all_groups': all_groups,
            'all_subjects': all_subjects,
            'group': group,
            'subject': subject,
            'students': students,
            'grades': grades,
            'grade_range': grade_range,
            'no_grades': no_grades,
            'stud_ave': stud_ave,
            'class_ave': class_ave,
        })

    return render(request, 'notes/modifygrades.html', context)


@login_required
def new_studentreport(request):
    user=request.user
    allgroups = Group.objects.filter(type="promo").all()
    context={
        'user':user,
        'allgroups':allgroups,
    }
    return render(request, 'notes/newstudentreport.html',context)


@login_required
def getnew_studentreport(request):
    user=request.user
    allgroups = Group.objects.filter(type="promo").all()
    context={
        'user':user,
        'allgroups':allgroups,
    }
    if request.method == "POST":
        group = Group.objects.filter(name=request.POST.get('class')).first()
        students = group.users.filter(user_type='student').order_by('last_name')
        context={
            'user':user,
            'allgroups':allgroups,
            'students':students,
        }
        return render(request, 'notes/getreport.html', context)
    else:
        return render(request, 'notes/newstudentreport.html',context)


def attendance_student(request):
    user = request.user
    absences = Presence.objects.filter(user=user, presence="absent",
                                       justified=False)
    lates = Presence.objects.filter(user=user, presence="late",
                                    justified=False)

    context = {'user': user, 'absences': absences, 'lates': lates}

    return render(request, 'attendance/attendance_student.html', context)


@login_required
def generate_student_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        user = get_object_or_404(CustomUser, id=student_id)
        user_promo = Group.objects.filter(type="promo", users=user).first()
        ues_average = []
        subj_average = []
        teachers = []
        subj_list = []
        no_note = True
        ues_list = []

        i = 0
        if user.user_type == 'student' and user_promo is not None:
            for unite in user_promo.ues.all():
                subj = unite.subjects.all()
                for j in range(len(subj)):
                    if Grade.objects.filter(subject=subj[j], user=user) and unite not in ues_list:
                        ues_list.append(unite)

            subj_list = [[] for _ in range(len(ues_list))]
            subj_average = [[] for _ in range(len(ues_list))]
            teachers = [[] for _ in range(len(ues_list))]
            for ue in ues_list:
                ave = 0.0
                sum = 0
                for subj in ue.subjects.all():
                    if Grade.objects.filter(subject=subj, user=user):
                        subj_list[i].append(subj)

                if subj_list[i]:
                    no_note = False
                    for s in subj_list[i]:
                        ave_s = 0.0
                        sum_coeff_s = 0
                        course = Course.objects.filter(subject=s).first()
                        if course:
                            teacher = course.teacher
                            teachers[i].append(f"{teacher.first_name} {teacher.last_name}")
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

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{user.first_name}_{user.last_name}_report.pdf"'

            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []

            # User Info
            user_info_text = f"<b><font color='darkblue'>Nom Prénom:</font></b> {user.last_name} {user.first_name}<br/><b><font color='darkblue'>Numéro étudiant:</font></b> {user.username}"
            user_info_para = Paragraph(user_info_text, getSampleStyleSheet()["BodyText"])
            elements.append(user_info_para)
            elements.append(Spacer(1, 12))  # Adding some space between user info and the rest of the content

            # Loop through UEs and Subjects to create the table
            for ue_index, ue in enumerate(ues_list):
                ue_title = Paragraph(f"UE: {ue.name}", getSampleStyleSheet()["Heading2"])
                elements.append(ue_title)

                data = [["UE", "Sujet", "Professeur", "Note Moyenne"]]
                for subj_index, subj in enumerate(subj_list[ue_index]):
                    if subj_index == 0:
                        data.append([ue.name, subj.name, teachers[ue_index][subj_index], subj_average[ue_index][subj_index]])
                    else:
                        data.append(["", subj.name, teachers[ue_index][subj_index], subj_average[ue_index][subj_index]])

                ue_table = Table(data, colWidths=[100, 200, 200, 100])
                ue_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(ue_table)

            # Build the PDF
            doc.build(elements)

            return response

    return HttpResponse(status=400)


def attendance_teacher(request):
    user = request.user
    current_time = timezone.now()
    three_hours_ago = current_time - timezone.timedelta(hours=3)

    sessions = Session.objects.annotate(
        end_time=ExpressionWrapper(F('date') + F('duration'),
                                   output_field=DateTimeField())
    ).filter(
        date__lt=current_time,
        course__teacher=user
    ).filter(
        Q(is_called_done=False) |
        Q(end_time__gt=three_hours_ago)
    ).order_by('-date')

    context = {'user': user, 'sessions': sessions}

    return render(request, 'attendance/attendance_teacher.html', context)


def class_call(request, id):
    user = request.user
    session = get_object_or_404(Session, pk=id)
    student_list = session.course.group.users.order_by('last_name')
    presences = Presence.objects.filter(session=session)
    presences_dict = {presence.user_id: presence for presence in presences}

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

    context = {'user': user, 'session': session, 'student_list': student_list,
               'presences_dict': presences_dict}

    return render(request, 'attendance/class_call.html', context)

""" Helper functions
"""

# Retrieve the group and subject based on the POST data
def get_group_and_subject(request):
    group_name = request.POST.get('group')
    subject_name = request.POST.get('subj')
    group = get_object_or_404(Group, name=group_name)
    subject = get_object_or_404(Subject, name=subject_name)
    return group, subject


# Retrieve students and their grades for a given group and subject
def get_students_and_grades(group, subject):
    students = group.users.filter(user_type='student').order_by('last_name')
    grades = [[] for _ in range(len(students))]
    no_grades = True

    for i, student in enumerate(students):
        student_grades = Grade.objects.filter(subject=subject, user=student)
        if student_grades.exists():
            no_grades = False
        grades[i] = list(student_grades)

    max_grades = max(
        len(student_grades) for student_grades in grades) if grades else 0

    # Fill empty grades slots with None
    for student_grades in grades:
        while len(student_grades) < max_grades:
            student_grades.append(None)

    return students, grades, no_grades, max_grades


# Calculate student averages and class averages
def calculate_averages(students, grades, max_grades):
    stud_ave = [calculate_student_average(student_grades) for student_grades in
                grades]
    class_ave = calculate_class_averages(grades, max_grades)
    return stud_ave, class_ave


# Calculate the average grade for a student
def calculate_student_average(grades):
    total_grade = 0
    total_coeff = 0
    for grade in grades:
        if grade:
            total_grade += grade.grade * grade.coeff
            total_coeff += grade.coeff
    if total_coeff == 0:
        return " "
    return round(total_grade / total_coeff, 2)


# Calculate the average grade for each grade column
def calculate_class_averages(grades, max_grades):
    class_averages = []
    for i in range(max_grades):
        total_grade = 0
        count = 0
        for student_grades in grades:
            if student_grades[i]:
                total_grade += student_grades[i].grade
                count += 1
        if count == 0:
            class_averages.append(" ")
        else:
            class_averages.append(round(total_grade / count, 2))
    return class_averages


# Get the user promo
def get_user_promo(user):
    return Group.objects.filter(type="promo", users=user).first()


# Get a list with all UEs
def get_ues_list(user, user_promo):
    ues_list = []
    for unite in user_promo.ues.all():
        for subj in unite.subjects.all():
            if Grade.objects.filter(subject=subj,
                                    user=user).exists() and unite not in ues_list:
                ues_list.append(unite)
                break
    return ues_list


# Get the subjects and averages
def get_subjects_and_averages(user, ues_list):
    subj_list = [[] for _ in range(len(ues_list))]
    subj_average = [[] for _ in range(len(ues_list))]
    teachers = [[] for _ in range(len(ues_list))]
    ues_average = []
    no_note = True

    for i, ue in enumerate(ues_list):
        ue_average = 0.0
        total_ue_coeff = 0

        for subj in ue.subjects.all():
            if Grade.objects.filter(subject=subj, user=user).exists():
                subj_list[i].append(subj)

        if subj_list[i]:
            no_note = False
            for subj in subj_list[i]:
                subj_avg, total_subj_coeff, teacher = calculate_subject_average(
                    user, subj)
                if teacher:
                    teachers[i].append(teacher)
                else:
                    teachers[i].append("-")
                subj_average[i].append(round(subj_avg, 2))
                ue_average += subj_avg * subj.coeff
                total_ue_coeff += subj.coeff

            if total_ue_coeff > 0:
                ue_average /= total_ue_coeff
                ues_average.append(round(ue_average, 2))

    return subj_list, subj_average, teachers, ues_average, no_note


# Calculate the subject average
def calculate_subject_average(user, subject):
    total_grade = 0
    total_coeff = 0
    teacher = None

    course = Course.objects.filter(subject=subject).first()
    if course:
        teacher = course.teacher.last_name

    for grade in Grade.objects.filter(subject=subject, user=user):
        total_grade += grade.grade * grade.coeff
        total_coeff += grade.coeff

    if total_coeff > 0:
        average = total_grade / total_coeff
    else:
        average = 0

    return average, total_coeff, teacher