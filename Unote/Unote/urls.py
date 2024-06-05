"""
URL configuration for Unote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path("", include("users.urls")),
    path("portal/", include("user_portal.urls")),
    path("administration/", include("administration.urls")),
]

handler400 = 'main.views.error_400'
handler403 = 'main.views.error_403'
handler404 = 'main.views.error_404'
handler405 = 'main.views.error_405'
handler500 = 'main.views.error_500'
