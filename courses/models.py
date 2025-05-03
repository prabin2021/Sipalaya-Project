from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='instructors/', blank=True, null=True)
    bio = models.TextField()
    experience = models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    DURATION_CHOICES = [
        ('short', 'Short-term (1-3 months)'),
        ('medium', 'Medium-term (3-6 months)'),
        ('long', 'Long-term (6+ months)'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='medium')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    syllabus = models.TextField(blank=True, help_text="Enter each syllabus item on a new line")
    prerequisites = models.TextField(blank=True, help_text="Enter each prerequisite on a new line")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    enrollment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class DemoClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='demo_classes')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demo_classes')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_students = models.IntegerField(default=10)
    current_students = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.date} {self.start_time}"
    
    class Meta:
        ordering = ['date', 'start_time']

class DemoClassRegistration(models.Model):
    demo_class = models.ForeignKey(DemoClass, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demo_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('demo_class', 'student')
    
    def __str__(self):
        return f"{self.student.username} - {self.demo_class}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.amount}"
    
    class Meta:
        ordering = ['-payment_date']

class CourseResource(models.Model):
    RESOURCE_TYPES = [
        ('video', 'Video'),
        ('document', 'Document'),
        ('presentation', 'Presentation'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('other', 'Other'),
    ]

    CATEGORIES = [
        ('lecture', 'Lecture Material'),
        ('reading', 'Reading Material'),
        ('practice', 'Practice Exercise'),
        ('assessment', 'Assessment'),
        ('supplementary', 'Supplementary Material'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='course_resources/')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)
    order = models.IntegerField(default=0)  # For ordering resources in a course

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} - {self.get_resource_type_display()}"

class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resource_categories')
    
    def __str__(self):
        return f"{self.name} - {self.course.title}"


