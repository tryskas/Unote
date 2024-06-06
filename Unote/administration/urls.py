from django.urls import path
from . import views

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
    path("search_subject/", views.search_subject, name="search_subject"),
    path("create_subject/", views.SubjectCreationView.as_view(),
         name="create_subject"),
    path("update_subject/<int:pk>/", views.SubjectUpdateView.as_view(),
         name="update_subject"),
]
