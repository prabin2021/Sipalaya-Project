from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.utils import timezone
from django.conf import settings

class DemoClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demo_class_instructor')
    max_participants = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class DemoClassSchedule(models.Model):
    demo_class = models.ForeignKey(DemoClass, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.demo_class.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['start_time']

class DemoClassBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demo_bookings', null=True)
    schedule = models.ForeignKey(DemoClassSchedule, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() if self.user else 'Anonymous'} - {self.schedule.demo_class.title}"

    class Meta:
        ordering = ['-created_at']

class DemoClassFeedback(models.Model):
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]

    booking = models.OneToOneField(DemoClassBooking, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    instructor_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    content_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback for {self.booking.schedule.demo_class.title} by {self.booking.user.get_full_name()}" 