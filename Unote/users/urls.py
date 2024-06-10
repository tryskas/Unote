from django.urls import path, include
from . import views
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Grade

app_name = "users"
urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password_change/', views.CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change_done/', views.CustomPasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path("register/", views.UserCreationView.as_view(), name="register"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
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


    
]
