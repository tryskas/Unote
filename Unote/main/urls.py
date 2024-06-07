from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("support/", views.HelpView.as_view(), name="help"),
    path("error_400/", views.error_400, name="error_400"),
    path("error_403/", views.error_403, name="error_403"),
    path("error_404/", views.error_404, name="error_404"),
    path("error_405/", views.error_405, name="error_405"),
    path("error_500/", views.error_500, name="error_500"),
]
