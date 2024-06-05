from django.db import models
from django.contrib.auth.models import AbstractUser



from django.db import models

class UE(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=255)
    coeff = models.IntegerField()
    ues = models.ManyToManyField(UE, related_name='Subjects')

    def __str__(self):
        return self.name

class Group(models.Model):
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    ues = models.ManyToManyField(UE, related_name='groups')
    users = models.ManyToManyField(CustomUser, related_name='users_groups')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Session(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    exam = models.BooleanField()
    date = models.DateTimeField()
    is_called_done = models.BooleanField(default=False)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    lesson= models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session du {self.start_time} au {self.end_time}"

class Grade(models.Model):
    grade = models.FloatField()
    coeff = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class Message(models.Model):
    objet = models.CharField(max_length=255)
    texte = models.TextField()
    date = models.DateTimeField()
    read = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Presence(models.Model):
    PRESENT = 'P'
    ABSENT = 'A'
    DELAY = 'D'
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (DELAY, 'DELAY'),
    ]

    presence = models.CharField(max_length=1, choices=STATUS_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    