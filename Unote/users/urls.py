from django.urls import path, include
from . import views

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
    path('profil/', views.ProfilView.as_view(), name='profil'),
    path('', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('enrollment/<int:enrollment_id>/add_grade/', GradeCreateView.as_view(), name='add_grade'),
    path('grade/<int:pk>/edit/', GradeUpdateView.as_view(), name='edit_grade'),
]