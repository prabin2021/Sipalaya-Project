from django.contrib import admin
from .models import Category, Course, Module, Lesson, Enrollment, Progress, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'price', 'duration', 'level', 'is_published', 'created_at')
    list_filter = ('category', 'level', 'is_published')
    search_fields = ('title', 'description', 'prerequisites')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    filter_horizontal = ('tags',)

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    ordering = ('course', 'order')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'duration', 'order', 'created_at')
    list_filter = ('module__course', 'module')
    search_fields = ('title', 'content')
    ordering = ('module', 'order')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed_at', 'is_active')
    list_filter = ('is_active', 'enrolled_at', 'completed_at')
    search_fields = ('student__email', 'course__title')
    ordering = ('-enrolled_at',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at')
    search_fields = ('enrollment__student__email', 'lesson__title')
    ordering = ('-completed_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('enrollment__student__email', 'enrollment__course__title', 'comment')
    ordering = ('-created_at',) 