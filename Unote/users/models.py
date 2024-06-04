'''from django.db import models
from django.forms import ModelForm
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    coeff = models.IntegerField()
    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Grade(models.Model):
    note = models.IntegerField()
    coeff = models.IntegerField()
    
class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['note']
'''
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Étudiant'),
        ('teacher', 'Professeur'),
        ('admin', 'Administrateur'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')


class UE(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    coeff = models.IntegerField()
    ues = models.ManyToManyField(UE, related_name='subjects')
    def __str__(self):
        return self.name

class Note(models.Model):
    note = models.FloatField()
    coeff = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
