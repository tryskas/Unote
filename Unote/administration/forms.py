from django import forms
from .models import Subject, UE, Group
from users.models import CustomUser
from .models import Course, Room, Session
from django.utils import timezone
from datetime import timedelta, datetime


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'coeff']
        labels = {
            'name': 'Nom de la matière',
            'coeff': 'Coefficient',
        }


class UEForm(forms.ModelForm):
    class Meta:
        model = UE
        fields = ['name', 'subjects']
        labels = {
            'name': 'Nom de l\'UE',
            'subjects': 'Matières associées',
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'type', 'users', 'ues']
        labels = {
            'name': 'Nom du groupe',
            'type': 'Type',
            'ues': 'UEs associées',
            'users': 'Utilisateurs membres du groupe'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = CustomUser.objects.order_by(
            'username')


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'group', 'teacher', 'subject']
        labels = {
            'name': 'Nom du cours',
            'group': 'Groupe associé',
            'teacher': 'Professeur du cours',
            'subject': 'Matière associée'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = CustomUser.objects.filter(
            user_type='teacher')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        labels = {
            'name': 'Nom de la salle',
        }


class SessionForm(forms.ModelForm):
    repeat = forms.BooleanField(required=False, label='Répéter cette session')
    repeat_interval = forms.IntegerField(required=False,
                                         label='Intervalle (jours)')
    repeat_duration = forms.IntegerField(required=False, label='Durée (jours)')

    class Meta:
        model = Session
        fields = ['course', 'date', 'duration', 'room', 'exam']
        labels = {
            'course': 'Cours',
            'date': 'Date et heure de la session',
            'duration': 'Durée (hh:mm:ss)',
            'room': 'Salle',
            'exam': 'Examen ?',
        }
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime(
                '%Y-%m-%dT%H:%M')
        else:
            self.fields['duration'].initial = "02:00:00"  # 2 hours default
