from django.contrib import admin
from .models import Teacher, Student, Code

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'subject', 'phone']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'phone', 'teacher', 'attend', 'homework', 'paid']

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ['codes','is_used']