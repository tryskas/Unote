from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Étudiant'),
        ('teacher', 'Professeur'),
        ('admin', 'Administrateur'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')


from django.db import models

class UE(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom
    
class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    coeff = models.IntegerField()
    ues = models.ManyToManyField(UE, related_name='matieres')

    def __str__(self):
        return self.nom

class Groupe(models.Model):
    type = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    ues = models.ManyToManyField(UE, related_name='groupes')

    def __str__(self):
        return self.nom

class Cours(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Session(models.Model):
    heure_debut = models.DateTimeField()
    heure_fin = models.DateTimeField()
    exam = models.BooleanField()

    def __str__(self):
        return f"Session du {self.heure_debut} au {self.heure_fin}"

class Salle(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Note(models.Model):
    note = models.FloatField()
    coeff = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

class Message(models.Model):
    objet = models.CharField(max_length=255)
    texte = models.TextField()
    date = models.DateTimeField()
    lu = models.BooleanField(default=False)
    favori = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Presence(models.Model):
    PRESENT = 'P'
    ABSENT = 'A'
    RETARD = 'R'
    STATUS_CHOICES = [
        (PRESENT, 'Présent'),
        (ABSENT, 'Absent'),
        (RETARD, 'En retard'),
    ]
    presence = models.CharField(max_length=1, choices=STATUS_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
