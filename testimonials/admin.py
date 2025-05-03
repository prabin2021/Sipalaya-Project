from django.contrib import admin
from .models import Testimonial, Review

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('student__username', 'course__title', 'content')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('student__username', 'course__title', 'content')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'
