from django.contrib import admin
from .models import Course, Category, Instructor, DemoClass, DemoClassRegistration, Enrollment, Payment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'price', 'skill_level', 'duration', 'is_active')
    list_filter = ('category', 'skill_level', 'duration', 'is_active')
    search_fields = ('title', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience')
    search_fields = ('name',)

@admin.register(DemoClass)
class DemoClassAdmin(admin.ModelAdmin):
    list_display = ('course', 'instructor', 'date', 'start_time', 'end_time', 'is_active')
    list_filter = ('date', 'is_active')
    search_fields = ('course__title', 'instructor__username')

@admin.register(DemoClassRegistration)
class DemoClassRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'demo_class', 'registered_at', 'attended')
    list_filter = ('attended', 'registered_at')
    search_fields = ('student__username', 'demo_class__course__title')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'progress', 'is_completed')
    list_filter = ('is_completed', 'enrolled_at')
    search_fields = ('student__username', 'course__title')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('student__username', 'course__title')
