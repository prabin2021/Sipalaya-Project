from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    DURATION_CHOICES = [
        ('short', 'Short-term (1-4 weeks)'),
        ('medium', 'Medium-term (5-8 weeks)'),
        ('long', 'Long-term (9+ weeks)'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    syllabus = models.TextField(default="Course syllabus will be provided soon.")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='courses_teaching')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    duration_weeks = models.PositiveIntegerField(help_text="Number of weeks", default=8)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    enrollment_deadline = models.DateField(default=timezone.now)
    prerequisites = models.TextField(blank=True, default="No prerequisites required")
    image = models.ImageField(upload_to='courses/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    demo_class_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"

class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"
        
    @property
    def is_active(self):
        """Check if the assignment is still active based on the due date."""
        return timezone.now() <= self.due_date

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('graded', 'Graded'),
        ('returned', 'Returned for Revision'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField()
    file = models.FileField(upload_to='submissions/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.email} - {self.assignment.title}"

class DemoClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='demo_classes')
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.date} {self.time}"
    
    @property
    def booked_count(self):
        return self.bookings.filter(status='confirmed').count()

class DemoClassBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    demo_class = models.ForeignKey(DemoClass, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demo_bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.email} - {self.demo_class}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('full', 'Full Payment'),
        ('installment', 'Installment Payment'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='full')
    total_installments = models.PositiveIntegerField(default=1)
    current_installment = models.PositiveIntegerField(default=1)
    next_installment_due = models.DateTimeField(null=True, blank=True)
    last_warning_sent = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    khalti_payment_id = models.CharField(max_length=100, blank=True)
    khalti_transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.email} - {self.amount}"
        
    def can_pay_next_installment(self):
        """Check if next installment can be paid."""
        return (
            self.payment_type == 'installment' and 
            self.status == 'completed' and 
            self.current_installment < self.total_installments
        )
    
    def get_next_installment_amount(self):
        """Calculate the amount for the next installment."""
        if not self.can_pay_next_installment():
            return 0
        return self.amount
    
    def is_installment_overdue(self):
        """Check if the current installment is overdue."""
        if not self.next_installment_due:
            return False
        return timezone.now() > self.next_installment_due
    
    def check_installment_completion(self):
        """Check if all installments are completed and update status if needed."""
        if (self.payment_type == 'installment' and 
            self.current_installment >= self.total_installments):
            self.status = 'completed'
            self.save(update_fields=['status'])
            return True
        return False
    
    @property
    def installment_number(self):
        """Alias for current_installment to maintain compatibility with templates."""
        return self.current_installment

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    invoice_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.email} - {self.invoice_number}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, related_name='enrollment')
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title}"

class LessonProgress(models.Model):
    """Model for tracking student progress in lessons."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'lesson')
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progress'

    def __str__(self):
        return f"{self.student.email} - {self.lesson.title}"

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f"CERT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class Review(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title} - {self.rating} stars"
