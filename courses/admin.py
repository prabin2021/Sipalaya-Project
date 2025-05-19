from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Category, Course, Module, Lesson, 
    Assignment, Submission, DemoClass, 
    DemoClassBooking, Payment, Invoice, Enrollment,
    LessonProgress, Certificate, Review
)
from instructor.models import InstructorProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'level', 'price', 'is_featured')
    list_filter = ('category', 'level', 'is_featured')
    search_fields = ('title', 'description', 'instructor__email')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('instructor', 'category')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    raw_id_fields = ('course',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    list_filter = ('module__course',)
    search_fields = ('title', 'module__title')
    raw_id_fields = ('module',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'due_date')
    list_filter = ('lesson__module__course',)
    search_fields = ('title', 'lesson__title')
    raw_id_fields = ('lesson',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'status')
    list_filter = ('status', 'assignment__lesson__module__course')
    search_fields = ('student__email', 'assignment__title')
    raw_id_fields = ('student', 'assignment')

@admin.register(DemoClass)
class DemoClassAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'time', 'capacity')
    list_filter = ('course',)
    search_fields = ('course__title',)
    raw_id_fields = ('course',)

@admin.register(DemoClassBooking)
class DemoClassBookingAdmin(admin.ModelAdmin):
    list_display = ('demo_class', 'student', 'status', 'booked_at')
    list_filter = ('status', 'demo_class__course')
    search_fields = ('student__email', 'demo_class__course__title')
    raw_id_fields = ('demo_class', 'student')

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'experience')
    search_fields = ('user__email', 'bio', 'experience')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__email', 'transaction_id')
    raw_id_fields = ('student',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'invoice_number', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__email', 'invoice_number')
    raw_id_fields = ('student',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed')
    list_filter = ('completed', 'course')
    search_fields = ('student__email', 'course__title')
    raw_id_fields = ('student', 'course')

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'lesson__module__course')
    search_fields = ('student__email', 'lesson__title')
    raw_id_fields = ('student', 'lesson')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'certificate_number', 'issued_at')
    search_fields = ('student__email', 'course__title', 'certificate_number')
    raw_id_fields = ('student', 'course')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'course')
    search_fields = ('student__email', 'course__title', 'comment')
    raw_id_fields = ('student', 'course')
