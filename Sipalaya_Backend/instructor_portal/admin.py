from django.contrib import admin
from .models import Course, Lesson, Resource, Assignment, CourseMaterial, Announcement

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at', 'is_active')
    list_filter = ('is_active', 'level')
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration')
    list_filter = ('course',)
    search_fields = ('title', 'content')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_at')
    list_filter = ('course',)
    search_fields = ('title',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'total_points')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_at')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'is_important')
    list_filter = ('course', 'is_important')
    search_fields = ('title', 'content')
