from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, CourseResource
from django.utils import timezone
# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses_taught") 

#     def __str__(self):
#         return self.title

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    has_completed_profile = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    has_completed_profile = models.BooleanField(default=False)  # Track if student filled details

    def __str__(self):
        return self.full_name if self.full_name else self.user.username
    
class InstructorProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    has_completed_profile = models.BooleanField(default=False)  # Track if student filled details

    def __str__(self):
        return self.full_name if self.full_name else self.user.username
class EnrolledCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # ✅ Ensure ForeignKey exists
    progress = models.FloatField(default=0.0)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Untitled Assignment')
    description = models.TextField(default='No description provided')
    due_date = models.DateTimeField(default=timezone.now)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    file = models.FileField(upload_to='assignments/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.course.title} - {self.title}"

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='certificates/')
    issued_at = models.DateField(auto_now_add=True)

    def __str__(self):
        # Access the 'title' from the related 'course' (which is a ForeignKey to Course)
        return f"Certificate - {self.student.username} - {self.course.course.title}"

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=True)  # Present or Absent

    def __str__(self):
        # Access the 'title' from the related 'course' (which is a ForeignKey to Course)
        return f"{self.student.username} - {self.course.course.title} - {self.date}"

class CompletedLesson(models.Model):
    enrolled_course = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE, related_name="completed_lessons", null=True,blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.IntegerField()  # Assuming lessons are identified by an ID
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - Lesson {self.lesson_id} Completed"

class Rubric(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='rubric')
    criterion = models.CharField(max_length=255)
    max_points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.criterion} - {self.max_points} points"
