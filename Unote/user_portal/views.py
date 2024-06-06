from django.views.generic.base import TemplateView


class DashboardView(TemplateView):
    template_name = "user_portal/dashboard.html"
