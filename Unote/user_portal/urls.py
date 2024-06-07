from django.urls import path
from . import views

app_name = "user_portal"
urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(),
         name="dashboard"),
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
]
