from django.contrib import admin
from .models import CustomUser, Grade, Room, Subject, UE, Group, Lesson, Message, Session, Presence
from django import forms

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')
    search_fields = ('username', 'email', 'first_name', 'last_name')

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

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    # Override the default widget for the users field
    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Users", False),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    form = GroupAdminForm


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'teacher', 'subject')
    search_fields = ('name', 'group__name', 'teacher__username', 'subject__name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('object', 'user', 'date')
    search_fields = ('object', 'user__username', 'date')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'exam', 'date', 'is_called_done', 'room', 'lesson')
    search_fields = ('start_time', 'end_time', 'room__name', 'lesson__name')

@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'presence', 'room')
    search_fields = ('user__username', 'session__start_time', 'session__end_time', 'room__name')
