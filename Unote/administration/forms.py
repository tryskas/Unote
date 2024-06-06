from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'coeff']
        labels = {
            'name': 'Nom de la matière',
            'coeff': 'Coefficient',
        }
