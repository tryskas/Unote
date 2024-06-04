from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Subject, Note, CustomUser, UE
from .forms import GradeForm
from django.shortcuts import render, redirect

def subject_list_view(request):
    user = request.user
    ue = UE.objects.all()
    subjects = Subject.objects.all()
    notes = Note.objects.all()
    
    
    context = {'user': user, 'subjects':subjects,'notes':notes,'ue':ue}
    #template_name = 'notes/subject_list.html'
    context_object_name = 'subject_list'
    return render(request,'notes/subject_list.html',context)


class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'notes/subject_detail.html'
    context_object_name = 'matiere'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matiere = self.get_object()
        context['enrollments'] = Enrollment.objects.filter(matiere=matiere)
        return context

class GradeCreateView(CreateView):
    model = Note
    form_class = GradeForm
    template_name = 'notes/add_grade.html'

    def form_valid(self, form):
        form.instance.enrollment = get_object_or_404(Enrollment, pk=self.kwargs['enrollment_id'])
        return super().form_valid(form)

    def get_success_url(self):
        enrollment = self.object.enrollment
        return reverse_lazy('subject_detail', kwargs={'pk': enrollment.subject.id})

class GradeUpdateView(UpdateView):
    model = Note
    form_class = GradeForm
    template_name = 'notes/edit_grade.html'

    def get_success_url(self):
        enrollment = self.object.enrollment
        return reverse_lazy('subject_detail', kwargs={'pk': enrollment.subject.id})
