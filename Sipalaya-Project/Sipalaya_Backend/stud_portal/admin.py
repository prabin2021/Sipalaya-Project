from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html
from .models import (EnrolledCourse, CompletedLesson, Assignment, Attendance,
                    InstructorProfile, Profile, StudentProfile, Certificate)
from django.contrib.auth.models import User

class CompletedLessonInline(admin.TabularInline):
    model = CompletedLesson
    extra = 0

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'has_completed_profile')
    list_filter = ('role', 'has_completed_profile')
    search_fields = ('user__username',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone', 'gender', 'has_completed_profile')
    list_filter = ('gender', 'has_completed_profile')
    search_fields = ('user__username', 'full_name', 'email')

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone', 'gender', 'has_completed_profile')
    list_filter = ('gender', 'has_completed_profile')
    search_fields = ('user__username', 'full_name', 'email')

@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress', 'enrollment_date')
    list_filter = ('enrollment_date',)
    search_fields = ('student__username', 'course__title')
    inlines = [CompletedLessonInline, AttendanceInline]

@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'enrolled_course', 'lesson_id', 'completed_at')
    list_filter = ('completed_at',)
    search_fields = ('student__username', 'enrolled_course__course__title')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'course', 'status', 'marks_obtained', 'due_date')
    list_filter = ('status', 'course', 'student')
    search_fields = ('title', 'student__username', 'course__course__title')
    readonly_fields = ('submitted_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('student__username', 'course__course__title')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('student__username', 'course__course__title')

# ✅ Custom Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'view_details_link')
    search_fields = ('username', 'email')

    def view_details_link(self, obj):
        return format_html('<a href="{}">View Details</a>', f"/admin/auth/user/{obj.id}/change/")
    view_details_link.short_description = "Student Details"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('auth/user/<int:student_id>/change/', self.admin_site.admin_view(self.student_detail_view), name="student-details"),
        ]
        return custom_urls + urls

    def student_detail_view(self, request, student_id):
        student = get_object_or_404(User, id=student_id)
        enrolled_courses = EnrolledCourse.objects.filter(student=student)
        attendance_records = Attendance.objects.filter(student=student)
        assignments = Assignment.objects.filter(student=student)
        
        context = {
            'student': student,
            'enrolled_courses': enrolled_courses,
            'attendance_records': attendance_records,
            'assignments': assignments,
            'title': f'Student Details - {student.username}',
            'opts': self.model._meta,
            'has_view_permission': True,
        }
        return render(request, 'admin/auth/user/change_form.html', context)

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, StudentAdmin)

def get_queryset(self, request):
    qs = super().get_queryset(request)
    if request.user.is_superuser:
        return qs  # Admin sees everything
    return qs.filter(course__instructor=request.user)  # Instructors see only their students
