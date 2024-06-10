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
    path('create_groups_csv/', views.create_groups_csv,
         name='create_groups_csv'),
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

    path("rooms/", views.rooms, name="rooms"),
    path("search_room/", views.search_room, name="search_room"),
    path("create_room/", views.RoomCreationView.as_view(),
         name="create_room"),
    path("update_room/<int:pk>/", views.RoomUpdateView.as_view(),
         name="update_room"),
    path('delete_room/<int:room_id>/', views.delete_room,
         name='delete_room'),

    path("sessions/", views.sessions, name="sessions"),
    path("search_session/", views.search_session, name="search_session"),
    path("create_session/", views.SessionCreationView.as_view(),
         name="create_session"),
    path("update_session/<int:pk>/", views.SessionUpdateView.as_view(),
         name="update_session"),
    path('delete_session/<int:session_id>/', views.delete_session,
         name='delete_session'),

    path('attendance_of/<int:user_id>/', views.attendance_of,
         name='attendance_of'),
]
