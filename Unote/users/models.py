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

class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    coeff = models.IntegerField()

    def __str__(self):
        return self.nom

class UE(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class User(models.Model):
    identifiant = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    mot_de_passe = models.CharField(max_length=255)

    def __str__(self):
        return self.identifiant

class Note(models.Model):
    note = models.FloatField()
    coeff = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
