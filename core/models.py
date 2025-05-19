from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')
    category = models.ForeignKey('courses.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='banners')
    button_text = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def link(self):
        if self.category:
            return f"/courses/?category={self.category.slug}"
        return "/courses/"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company}"

class Statistic(models.Model):
    title = models.CharField(max_length=100)
    value = models.PositiveIntegerField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title}: {self.value}"

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class CompanyInfo(models.Model):
    mission = models.TextField(help_text="Company's mission statement")
    vision = models.TextField(help_text="Company's vision statement")
    history = models.TextField(help_text="Company's history and background")
    established_date = models.DateField()
    
    class Meta:
        verbose_name_plural = 'Company Information'
    
    def __str__(self):
        return "Company Information"

class Milestone(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class", blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'date']
    
    def __str__(self):
        return f"{self.date.year}: {self.title}"

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('instructor', 'Instructor'),
        ('management', 'Management'),
        ('support', 'Support Staff'),
    ]
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    designation = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team/', blank=True)
    bio = models.TextField()
    qualifications = models.TextField()
    achievements = models.TextField()
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_key_member = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.designation}"

class Partnership(models.Model):
    PARTNERSHIP_TYPE_CHOICES = [
        ('company', 'IT Company'),
        ('certification', 'Certification Body'),
        ('academic', 'Academic Institution'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=PARTNERSHIP_TYPE_CHOICES)
    logo = models.ImageField(upload_to='partners/')
    description = models.TextField()
    website_url = models.URLField()
    partnership_date = models.DateField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Partnerships'
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Certification(models.Model):
    name = models.CharField(max_length=100)
    provider = models.ForeignKey(Partnership, on_delete=models.CASCADE, related_name='certifications')
    description = models.TextField()
    logo = models.ImageField(upload_to='certifications/')
    validity_period = models.PositiveIntegerField(help_text="Validity in months", null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} by {self.provider.name}"

class Contact(models.Model):
    PURPOSE_CHOICES = [
        ('course', 'Course Inquiry'),
        ('support', 'Technical Support'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_purpose_display()}"

class AlumniSuccessStory(models.Model):
    name = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()
    current_position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='alumni/', blank=True)
    story = models.TextField()
    achievements = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-graduation_year']
        verbose_name_plural = 'Alumni Success Stories'
    
    def __str__(self):
        return f"{self.name} - {self.current_position} at {self.company}"
