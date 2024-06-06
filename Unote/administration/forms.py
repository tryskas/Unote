from django import forms
from .models import Subject, UE


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
