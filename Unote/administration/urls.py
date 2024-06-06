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
    path("search_ue/", views.search_ue, name="search_ue"),
    path("create_ue/", views.UECreationView.as_view(), name="create_ue"),
    path("update_ue/<int:pk>/", views.UEUpdateView.as_view(),
         name="update_ue"),
    path('delete_ue/<int:ue_id>/', views.delete_ue, name='delete_ue'),
    path("subjects/", views.subjects, name="subjects"),
    path("search_subject/", views.search_subject, name="search_subject"),
    path("create_subject/", views.SubjectCreationView.as_view(),
         name="create_subject"),
    path("update_subject/<int:pk>/", views.SubjectUpdateView.as_view(),
         name="update_subject"),
    path('delete_subject/<int:subject_id>/', views.delete_subject,
         name='delete_subject'),
]
