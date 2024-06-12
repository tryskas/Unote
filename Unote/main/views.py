from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class HelpView(TemplateView):
    template_name = "main/help.html"


def error_400(request, exception=None):
    return render(request, 'main/400.html', status=400)


def error_403(request, exception=None):
    return render(request, 'main/403.html', status=403)


def error_404(request, exception=None):
    return render(request, 'main/404.html', status=404)


def error_405(request, exception=None):
    return render(request, 'main/405.html', status=405)


def error_500(request, exception=None):
    return render(request, 'main/500.html', status=500)
