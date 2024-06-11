from django.contrib import admin
from .models import (Grade, Room, Subject, UE, Group, Course, Message,
                     Session, Presence)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'grade')
    search_fields = ('user__username', 'subject__name')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'coeff')
    search_fields = ('name', 'coeff')


@admin.register(UE)
class UEAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'teacher', 'subject')
    search_fields = ('name', 'group__name', 'teacher__username',
                     'subject__name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('objet', 'user', 'date')
    search_fields = ('objet', 'user__username', 'date')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'duration', 'exam', 'is_called_done',
                    'room', 'course')
    search_fields = ('date', 'room__name', 'course__name')


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'justified', 'presence')
    search_fields = ('user__username', 'session__start_time',
                     'session__end_time')
