from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html
from .models import EnrolledCourse, CompletedLesson, Assignment, Attendance
from django.contrib.auth.models import User

class CompletedLessonInline(admin.TabularInline):
    model = CompletedLesson
    extra = 0  # No empty fields

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
# ✅ Custom Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'view_details_link')  # Clickable link
    search_fields = ('username', 'email')

    def view_details_link(self, obj):
        """Generates a clickable link in the admin panel"""
        return format_html('<a href="{}">View Details</a>', f"/admin/stud_portal/student/{obj.id}/details/")
    view_details_link.short_description = "Student Details"

    def get_urls(self):
        """Add a custom URL to view student details."""
        urls = super().get_urls()
        custom_urls = [
            path('student/<int:student_id>/details/', self.admin_site.admin_view(self.student_detail_view), name="student_detail"),
        ]
        return custom_urls + urls

    def student_detail_view(self, request, student_id):
        """Custom page showing full student details"""
        student = get_object_or_404(User, id=student_id)
        enrolled_courses = EnrolledCourse.objects.filter(student=student)
        attendance_records = Attendance.objects.filter(student=student)
        assignments = Assignment.objects.filter(student=student)
        course_progress = {course: self.calculate_progress(course, student) for course in enrolled_courses}
        context = {
            'student': student,
            'enrolled_courses': enrolled_courses,
            'attendance_records': attendance_records,
            'assignments': assignments,
            'course_progress': course_progress 
        }
        return render(request, 'admin/student_detail.html', context)

# ✅ Register the custom StudentAdmin
admin.site.unregister(User)
admin.site.register(User, StudentAdmin)
from django.contrib import admin
from .models import EnrolledCourse, Course

@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_course_title', 'get_instructor', 'get_category', 'progress')

    def get_course_title(self, obj):
        return obj.course.title

    def get_instructor(self, obj):
        return obj.course.instructor.name if obj.course.instructor else "No Instructor"

    def get_category(self, obj):
        return obj.course.category.name if obj.course.category else "No Category"

    get_course_title.short_description = 'Course'
    get_instructor.short_description = 'Instructor'
    get_category.short_description = 'Category'

# ✅ CompletedLesson Admin
@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson_id')
    search_fields = ('student__username', 'lesson_id')


# ✅ Assignment Admin
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'file', 'submitted_at')
    search_fields = ('student__username', 'course__title')
    list_filter = ('course',)


# ✅ Attendance Admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    search_fields = ('student__username',)
    list_filter = ('date', 'status')


def get_queryset(self, request):
    qs = super().get_queryset(request)
    if request.user.is_superuser:
        return qs  # Admin sees everything
    return qs.filter(course__instructor=request.user)  # Instructors see only their students
