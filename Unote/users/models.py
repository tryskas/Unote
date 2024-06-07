from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Étudiant'),
        ('teacher', 'Professeur'),
        ('admin', 'Administrateur'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,
                                 default='student')

    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"
