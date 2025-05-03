from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Testimonial(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Testimonial by {self.student.get_full_name()} for {self.course.title}"

    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.student.get_full_name()} for {self.course.title}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('student', 'course')  # One review per student per course
