from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from users.models import Subject, Grade, UE, Group
from django.shortcuts import render


class DashboardView(TemplateView):
    template_name = "user_portal/dashboard.html"


@login_required
def studentview(request):
    user = request.user
    ue = UE.objects.all()
    subjects = Subject.objects.all()
    grades = Grade.objects.all()
    user_promo = Group.objects.filter(type="promo", users=user).first()

    context = {'user': user, 'subjects': subjects, 'grades': grades, 'ue': ue,
               'user_promo': user_promo}
    return render(request, 'user_portal/studentview.html',
                  context)