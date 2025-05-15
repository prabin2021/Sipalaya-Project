from django.db import models
from django.utils import timezone

class PlacementService(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CompanyPartnership(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class JobListing(models.Model):
    company = models.ForeignKey(CompanyPartnership, on_delete=models.CASCADE, related_name='job_listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=[
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ])
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

class AlumniSuccessStory(models.Model):
    name = models.CharField(max_length=200)
    graduation_year = models.PositiveIntegerField()
    current_position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    story = models.TextField()
    image = models.ImageField(upload_to='alumni_stories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.current_position} at {self.company}"

class JobApplication(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='job_applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'applicant']

    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.job.title}"
