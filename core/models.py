from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Banner(models.Model):
    """Homepage banner model."""
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('banner')
        verbose_name_plural = _('banners')
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Feature(models.Model):
    """Homepage feature model."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text=_('Font Awesome icon class'))
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """Testimonial model."""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('testimonial')
        verbose_name_plural = _('testimonials')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.role}"

class FAQ(models.Model):
    """FAQ model."""
    question = models.CharField(max_length=200)
    answer = RichTextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('GENERAL', _('General')),
            ('COURSES', _('Courses')),
            ('PAYMENT', _('Payment')),
            ('TECHNICAL', _('Technical')),
        ]
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.question

class Contact(models.Model):
    """Contact form submission model."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class SiteSetting(models.Model):
    """Site settings model."""
    site_name = models.CharField(max_length=100)
    site_description = models.TextField()
    logo = models.ImageField(upload_to='site/')
    favicon = models.ImageField(upload_to='site/')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('site setting')
        verbose_name_plural = _('site settings')
    
    def __str__(self):
        return self.site_name 