from django.contrib import admin
from .models import EnrolledCourse, CompletedLesson, Assignment, Attendance

@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_date', 'progress', 'is_completed')
    list_filter = ('is_completed', 'course')
    search_fields = ('student__username', 'course__title')

@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed_date')
    list_filter = ('lesson__course',)
    search_fields = ('student__username', 'lesson__title')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'submitted_date', 'grade')
    list_filter = ('course', 'graded')
    search_fields = ('student__username', 'course__title')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'is_present')
    list_filter = ('course', 'is_present', 'date')
    search_fields = ('student__username', 'course__title')
