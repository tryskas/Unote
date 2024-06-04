from django.db import models
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
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['name']