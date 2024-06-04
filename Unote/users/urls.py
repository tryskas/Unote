from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    path('notes/', views.SubjectListView.as_view(), name='subject_list'),
    path('notes/subject/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('notes/enrollment/<int:enrollment_id>/add_grade/', views.GradeCreateView.as_view(), name='add_grade'),
    path('notes/grade/<int:pk>/edit/', views.GradeUpdateView.as_view(), name='edit_grade'),
]