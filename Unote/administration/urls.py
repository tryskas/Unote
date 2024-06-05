from django.urls import path, include
from . import views
from django.shortcuts import render, get_object_or_404

app_name = "administration"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("profiles/", views.profiles, name="profiles"),
    path('search_user/', views.search_user, name='search_user'),
    path("groups/", views.groups, name="groups"),
    path("courses/", views.courses, name="courses"),
    path("absences/", views.absences, name="absences"),
    path("eus/", views.eus, name="eus"),
    path("subjects/", views.subjects, name="subjects"),
]
