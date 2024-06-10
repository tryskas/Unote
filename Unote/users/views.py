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
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Subject, Grade, UE, Group, Lesson, CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

#Display the students average grades
@login_required
def studentview(request):
    user = request.user

    if user.user_type != 'student':
        return render(request, 'notes/studentview.html', {'user': user})

    user_promo = get_user_promo(user)
    if not user_promo:
        return render(request, 'notes/studentview.html', {'user': user})

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

    return render(request, 'notes/studentview.html', context)


#Choose options for the new grade
@login_required
def profview(request):
    user = request.user
    lessons = Lesson.objects.filter(teacher=user)
    subjects = [lesson.subject for lesson in lessons]

    groups = list({lesson.group for lesson in lessons if lesson.group.type == "promo"})

    all_subjects = Subject.objects.all()
    all_groups = Group.objects.filter(type="promo")

    context = {
        'user': user,
        'subjects': subjects,
        'groups': groups,
        'allsubj': all_subjects,
        'allgroups': all_groups,
    }

    return render(request, 'notes/profview.html', context)

#Home page for teachers
@login_required
def profviewhome(request):
    user = request.user
    context = {
        'user':user,
    }
    return render(request,'notes/profviewhome.html',context)

#Enter grades for each student
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

#Saving the grades
@login_required
def success_grades(request):
    user = request.user

    if request.method == "POST":
        group_name = request.POST.get('group')
        subject_name = request.POST.get('subject')
        coefficient = request.POST.get('coefficient')

        group = get_object_or_404(Group, name=group_name)
        subject = get_object_or_404(Subject, name=subject_name)

        students = group.users.filter(user_type='student').order_by('last_name')

        for student in students:
            grade_value = request.POST.get(str(student.id))
            if grade_value:
                grade=Grade.objects.create(
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

#Display all students grades
@login_required
def profview_grades(request):
    user = request.user
    groups = Group.objects.filter(type="promo").all()
    subjects = Subject.objects.all()
    no_grades = True
    context = {
        'user': user,
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


#Delete selected grades
@login_required
def delete_selected_grades(request):
    if request.method == 'POST':
        grades_to_delete = request.POST.getlist('grades_to_delete')
        if grades_to_delete:
            Grade.objects.filter(pk__in=grades_to_delete).delete()
        return redirect('users:modify_grades')
    return redirect('users:modify_grades')


#Display grades, possibility to delete
@login_required
def modify_grades(request):
    user = request.user
    groups = Group.objects.filter(type="promo").all()
    subjects = Subject.objects.all()
    no_grades = True
    context = {
        'user': user,
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

@login_required
def generate_student_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        user = CustomUser.objects.get(id=student_id)
        user_promo = get_user_promo(user)

        if user.user_type != 'student' or not user_promo:
            return HttpResponse("User is not a student or no promo group found.", status=400)

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

        html_content = render_to_string('notes/reportpage.html', context)
        filename = f'{user.first_name}-{user.last_name}-report.html'

        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    return HttpResponse("Invalid request method.", status=405)

""" Helper functions
"""
#Retrieve the group and subject based on the POST data
def get_group_and_subject(request):
    group_name = request.POST.get('group')
    subject_name = request.POST.get('subj')
    group = get_object_or_404(Group, name=group_name)
    subject = get_object_or_404(Subject, name=subject_name)
    return group, subject

#Retrieve students and their grades for a given group and subject
def get_students_and_grades(group, subject):
    students = group.users.filter(user_type='student').order_by('last_name')
    grades = [[] for _ in range(len(students))]
    no_grades = True
    
    for i, student in enumerate(students):
        student_grades = Grade.objects.filter(subject=subject, user=student)
        if student_grades.exists():
            no_grades = False
        grades[i] = list(student_grades)
    
    max_grades = max(len(student_grades) for student_grades in grades) if grades else 0
    
    # Fill empty grades slots with None
    for student_grades in grades:
        while len(student_grades) < max_grades:
            student_grades.append(None)
    
    return students, grades, no_grades, max_grades

#Calculate student averages and class averages
def calculate_averages(students, grades, max_grades):
    stud_ave = [calculate_student_average(student_grades) for student_grades in grades]
    class_ave = calculate_class_averages(grades, max_grades)
    return stud_ave, class_ave

#Calculate the average grade for a student
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

#Calculate the average grade for each grade column
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

#Get the user promo
def get_user_promo(user):
    return Group.objects.filter(type="promo", users=user).first()

#Get a list with all UEs
def get_ues_list(user, user_promo):
    ues_list = []
    for unite in user_promo.ues.all():
        for subj in unite.Subjects.all():
            if Grade.objects.filter(subject=subj, user=user).exists() and unite not in ues_list:
                ues_list.append(unite)
                break
    return ues_list

#Get the subjects and averages
def get_subjects_and_averages(user, ues_list):
    subj_list = [[] for _ in range(len(ues_list))]
    subj_average = [[] for _ in range(len(ues_list))]
    teachers = [[] for _ in range(len(ues_list))]
    ues_average = []
    no_note = True

    for i, ue in enumerate(ues_list):
        ue_average = 0.0
        total_ue_coeff = 0

        for subj in ue.Subjects.all():
            if Grade.objects.filter(subject=subj, user=user).exists():
                subj_list[i].append(subj)

        if subj_list[i]:
            no_note = False
            for subj in subj_list[i]:
                subj_avg, total_subj_coeff, teacher = calculate_subject_average(user, subj)
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

#Calculate the subject average
def calculate_subject_average(user, subject):
    total_grade = 0
    total_coeff = 0
    teacher = None

    lesson = Lesson.objects.filter(subject=subject).first()
    if lesson:
        teacher = lesson.teacher.last_name

    for grade in Grade.objects.filter(subject=subject, user=user):
        total_grade += grade.grade * grade.coeff
        total_coeff += grade.coeff

    if total_coeff > 0:
        average = total_grade / total_coeff
    else:
        average = 0

    return average, total_coeff, teacher
"""
"""



class UserCreationView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        if (self.object.user_type == 'student' or
                self.object.user_type == 'teacher'):
            return reverse_lazy('user_portal:dashboard')
        elif self.object.user_type == 'admin':
            return reverse_lazy('administration:dashboard')
        else:
            return reverse_lazy('main:error_400')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

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
