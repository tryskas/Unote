from django.urls import path
from . import views

app_name = "user_portal"
urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(),
         name="dashboard"),
    path('notes/', views.student_view, name="notes"),
    path('attendance_student/', views.attendance_student,
         name="attendance_student"),
    path('attendance_teacher/', views.attendance_teacher,
         name="attendance_teacher"),
    path('class_call/<int:id>', views.class_call, name='class_call'),
]
