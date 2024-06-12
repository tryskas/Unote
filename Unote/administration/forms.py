from django import forms
from .models import Subject, UE, Group
from users.models import CustomUser
from .models import Course, Room, Session
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.models import Q, F, ExpressionWrapper, DateTimeField


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


class GroupFormCSV(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'type']
        labels = {
            'name': 'Nom du groupe',
            'type': 'Type',
        }


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
    repeat_duration = forms.IntegerField(required=False,
                                         label='Nombre total de sessions à '
                                               'créer')

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

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        room = cleaned_data.get('room')
        duration = cleaned_data.get('duration')
        teacher = cleaned_data.get('course').teacher if cleaned_data.get(
            'course') else None
        group = cleaned_data.get('course').group if cleaned_data.get(
            'course') else None
        repeat = cleaned_data.get('repeat')
        repeat_interval = cleaned_data.get('repeat_interval')
        repeat_duration = cleaned_data.get('repeat_duration')

        if date and duration:
            end_of_session = date + duration
            sessions_to_check = [(date, end_of_session)]

            # If repeat is True, add the repeated sessions to the list to check
            if repeat and repeat_interval and repeat_duration:
                current_date = date
                for _ in range(repeat_duration):
                    current_date += timedelta(days=repeat_interval)
                    end_of_session = current_date + duration
                    sessions_to_check.append((current_date, end_of_session))

            conflicting_dates = {
                "room": [],
                "teacher": [],
                "group": []
            }

            for start_date, end_date in sessions_to_check:
                if room:
                    conflicting_sessions = self.get_conflicting_sessions(
                        room=room, date=start_date, end_of_session=end_date)
                    if conflicting_sessions.exists():
                        conflicting_dates["room"].append(start_date)

                if teacher:
                    conflicting_sessions = self.get_conflicting_sessions(
                        teacher=teacher, date=start_date,
                        end_of_session=end_date)
                    if conflicting_sessions.exists():
                        conflicting_dates["teacher"].append(start_date)

                if group:
                    conflicting_sessions = self.get_conflicting_sessions(
                        group=group, date=start_date, end_of_session=end_date)
                    if conflicting_sessions.exists():
                        conflicting_dates["group"].append(start_date)

            if conflicting_dates["room"]:
                raise ValidationError(
                    f"La salle est déjà prise aux dates suivantes : {', '.join([date.strftime('%Y-%m-%d %H:%M') for date in conflicting_dates['room']])}.")

            if conflicting_dates["teacher"]:
                raise ValidationError(
                    f"Le professeur a déjà un cours aux dates suivantes : {', '.join([date.strftime('%Y-%m-%d %H:%M') for date in conflicting_dates['teacher']])}.")

            if conflicting_dates["group"]:
                raise ValidationError(
                    f"Ce groupe a déjà un cours aux dates suivantes : {', '.join([date.strftime('%Y-%m-%d %H:%M') for date in conflicting_dates['group']])}.")

        return cleaned_data

    def get_conflicting_sessions(self, date, end_of_session, room=None,
                                 teacher=None, group=None):
        queryset = Session.objects.annotate(
            end_date=ExpressionWrapper(F('date') + F('duration'),
                                       output_field=DateTimeField())
        ).filter(
            Q(date__lt=end_of_session, end_date__gt=date)
        )

        if room:
            queryset = queryset.filter(room=room)

        if teacher:
            queryset = queryset.filter(course__teacher=teacher)

        if group:
            queryset = queryset.filter(course__group=group)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        return queryset
