from django.urls import path
from . import views

app_name = "administration"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("profiles/", views.profiles, name="profiles"),
    path('search_user/', views.search_user, name='search_user'),
    path("groups/", views.groups, name="groups"),
    path("search_group/", views.search_group, name="search_group"),
    path("create_group/", views.GroupCreationView.as_view(),
         name="create_group"),
    path("update_group/<int:pk>/", views.GroupUpdateView.as_view(),
         name="update_group"),
    path('delete_group/<int:group_id>/', views.delete_group,
         name='delete_group'),

    path("courses/", views.courses, name="courses"),
    path("search_course/", views.search_course, name="search_course"),
    path("create_course/", views.CourseCreationView.as_view(),
         name="create_course"),
    path("update_course/<int:pk>/", views.CourseUpdateView.as_view(),
         name="update_course"),
    path('delete_course/<int:course_id>/', views.delete_course,
         name='delete_course'),

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
    path('attendance_teacher/', views.attendance_teacher,
         name="attendance_teacher"),
    path('class_call/<int:id>', views.class_call, name='class_call'),
    path('attendance_student/', views.attendance_student,
         name="attendance_student"),
    path('attendance_admin/', views.attendance_admin, name="attendance_admin"),
    path('attendance_of/<str:username>/', views.attendance_of,
         name='attendance_of'),
]
