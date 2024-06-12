from django.db import models
from users.models import CustomUser


class Subject(models.Model):
    name = models.CharField(max_length=255)
    coeff = models.IntegerField()

    def __str__(self):
        return self.name


class UE(models.Model):
    name = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject, related_name='ues')

    def __str__(self):
        return self.name


class Group(models.Model):
    GROUP_TYPE_CHOICES = (
        ('promo', 'Promotion'),
        ('td_group', 'Groupe de TD'),
        ('tp_group', 'Groupe de TP'),
        ('generic_group', 'Groupe générique'),
    )
    type = models.CharField(max_length=255, choices=GROUP_TYPE_CHOICES,
                            default='promo')
    name = models.CharField(max_length=255)
    ues = models.ManyToManyField(UE, related_name='groups')
    users = models.ManyToManyField(CustomUser, related_name='users_groups')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Session(models.Model):
    date = models.DateTimeField()
    duration = models.DurationField()
    exam = models.BooleanField()
    is_called_done = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session du {self.date} (durée : {self.duration} minute(s)))"


class Grade(models.Model):
    grade = models.FloatField()
    coeff = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Message(models.Model):
    objet = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField()
    read = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Presence(models.Model):
    PRESENCE_TYPE = (
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('late', 'En retard'),
    )
    presence = models.CharField(max_length=30, choices=PRESENCE_TYPE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    justified = models.BooleanField(default=False)
