from django.db import models
from django.conf import settings
from courses.models import Course

# Create your models here.

class Testimonial(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_testimonials')
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    is_video = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Testimonial by {self.student.get_full_name()}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedback_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"Review by {self.student.get_full_name()} for {self.course.title}"
    
    def get_rating_display(self):
        return '★' * self.rating + '☆' * (5 - self.rating)
