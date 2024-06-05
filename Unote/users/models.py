from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Etudiant'),
        ('teacher', 'Professeur'),
        ('admin', 'Administration'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')

