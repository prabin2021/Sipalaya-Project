from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses_taught") 

#     def __str__(self):
#         return self.title

class EnrolledCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # ✅ Ensure ForeignKey exists
    progress = models.FloatField(default=0.0)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Assignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        # Access the 'title' from the related 'course' (which is a ForeignKey to Course)
        return f"{self.student.username} - {self.course.course.title} Assignment"

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
