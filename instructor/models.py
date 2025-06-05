from django.db import models
from django.conf import settings
from django.utils import timezone

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('video', 'Video'),
        ('document', 'Document'),
        ('link', 'External Link'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class AssignmentFeedback(models.Model):
    submission = models.OneToOneField('courses.Submission', on_delete=models.CASCADE, related_name='feedback')
    feedback = models.TextField()
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Feedback for {self.submission}"

class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='instructor_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

    class Meta:
        verbose_name = 'Instructor Profile'
        verbose_name_plural = 'Instructor Profiles'
