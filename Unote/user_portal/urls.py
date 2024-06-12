from django.urls import path
from . import views

app_name = "user_portal"
urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("my_account/", views.MyAccountView.as_view(),
         name="my_account"),
    path('notes/', views.studentview, name="notes"),
    path('notes/prof/', views.profview, name='profview'),
    path('notes/prof/entergrades', views.profview_entergrades, name='profview_entergrades'),
    path('notes/prof/grades', views.profview_grades, name='profview_grades'),
    path('notes/prof/success', views.success_grades, name='success_grades'),
    path('attendance_student/', views.attendance_student,
         name="attendance_student"),
    path('attendance_teacher/', views.attendance_teacher,
         name="attendance_teacher"),
    path('class_call/<int:id>', views.class_call, name='class_call'),

    path('notes/student/', views.studentview, name='studentview'),
    path('notes/home/', views.profviewhome, name='profviewhome'),
    path('notes/new_grade', views.profview, name='profview'),
    path('notes/new_grade/enter_grades', views.profview_entergrades, name='profview_entergrades'),
    path('notes/new_grade/enter_grades/success', views.success_grades, name='success_grades'),
    path('notes/view_grades', views.profview_grades, name='profview_grades'),
    path('notes/modify_grades/', views.modify_grades, name='modify_grades'),
    path('notes/modify_grades/delete_selected_grades/', views.delete_selected_grades, name='delete_selected_grades'),
    path('notes/new_report/', views.new_studentreport, name='new_studentreport'),
    path('notes/new_report/get/', views.getnew_studentreport, name='getnew_studentreport'),
    path('notes/new_report/get/generate/', views.generate_student_view, name='generate_student_view'),
    path('schedule/', views.weekly_schedule, name='weekly_schedule'),
]
