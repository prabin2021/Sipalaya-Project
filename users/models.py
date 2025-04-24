from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom user model for the LMS."""
    
    class UserType(models.TextChoices):
        STUDENT = 'STUDENT', _('Student')
        INSTRUCTOR = 'INSTRUCTOR', _('Instructor')
        ADMIN = 'ADMIN', _('Admin')
    
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(max_length=200, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name 