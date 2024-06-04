from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Subject, Enrollment, Grade
from .forms import GradeForm

class SubjectListView(ListView):
    model = Subject
    template_name = 'notes/subject_list.html'
    context_object_name = 'subject_list'

class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'notes/subject_detail.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        context['enrollments'] = Enrollment.objects.filter(subject=subject)
        return context

class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'notes/add_grade.html'

    def form_valid(self, form):
        form.instance.enrollment = get_object_or_404(Enrollment, pk=self.kwargs['enrollment_id'])
        return super().form_valid(form)

    def get_success_url(self):
        enrollment = self.object.enrollment
        return reverse_lazy('subject_detail', kwargs={'pk': enrollment.subject.id})

class GradeUpdateView(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'notes/edit_grade.html'

    def get_success_url(self):
        enrollment = self.object.enrollment
        return reverse_lazy('subject_detail', kwargs={'pk': enrollment.subject.id})
