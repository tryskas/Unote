from django.urls import path
from . import views

app_name = "user_portal"
urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(),
         name="dashboard"),
    path('notes/', views.studentview, name="notes")
]
