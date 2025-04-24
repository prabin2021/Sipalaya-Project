from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class Category(models.Model):
    """Course category model."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    
    def __str__(self):
        return self.name

class Course(models.Model):
    """Course model."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    description = RichTextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.IntegerField(help_text=_('Duration in weeks'))
    level = models.CharField(
        max_length=20,
        choices=[
            ('BEGINNER', _('Beginner')),
            ('INTERMEDIATE', _('Intermediate')),
            ('ADVANCED', _('Advanced')),
        ]
    )
    prerequisites = models.TextField(blank=True)
    what_you_will_learn = RichTextField()
    tags = TaggableManager()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
    
    def __str__(self):
        return self.title

class Module(models.Model):
    """Course module model."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    """Course lesson model."""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = RichTextField()
    video_url = models.URLField(blank=True)
    duration = models.IntegerField(help_text=_('Duration in minutes'))
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"

class Enrollment(models.Model):
    """Course enrollment model."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('enrollment')
        verbose_name_plural = _('enrollments')
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title}"

class Progress(models.Model):
    """Course progress model."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('progress')
        verbose_name_plural = _('progress')
        unique_together = ['enrollment', 'lesson']
    
    def __str__(self):
        return f"{self.enrollment.student.email} - {self.lesson.title}"

class Review(models.Model):
    """Course review model."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        unique_together = ['enrollment']
    
    def __str__(self):
        return f"{self.enrollment.student.email} - {self.enrollment.course.title}" 