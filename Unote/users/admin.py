from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
admin.site.register(CustomUser, CustomUserAdmin)
from .models import CustomUser, Grade, Room, Subject, UE, Group, Lesson, Message, Session, Presence

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Type d\'utilisateur', {'fields': ('user_type',)}),
    )
    
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'Subject', 'grade')
    search_fields = ('user__username', 'Subject__name')

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

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'teacher', 'subject')
    search_fields = ('name', 'group__name', 'teacher__username', 'subject__name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('objet', 'user', 'date')
    search_fields = ('objet', 'user__username', 'date')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'exam', 'date', 'is_called_done', 'room', 'lesson')
    search_fields = ('start_time', 'end_time', 'room__name', 'lesson__name')

@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'presence', 'Room')
    search_fields = ('user__username', 'session__start_time', 'session__end_time', 'Room__name')