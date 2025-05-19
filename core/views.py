from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Banner, Testimonial, Statistic, Service, CompanyInfo, TeamMember
from courses.models import Course, Category
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Create your views here.

def home(request):
    featured_courses = Course.objects.all()[:6]  # Get up to 6 courses
    categories = Category.objects.all()
    banners = Banner.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    statistics = Statistic.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'banners': banners,
        'services': services,
        'statistics': statistics,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    company_info = CompanyInfo.objects.first()
    team_members = TeamMember.objects.filter(is_key_member=True)
    return render(request, 'about.html', {
        'company_info': company_info,
        'team_members': team_members
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Prepare email content
            context = {
                'name': contact.name,
                'email': contact.email,
                'purpose': contact.get_purpose_display(),
                'message': contact.message,
                'created_at': contact.created_at,
            }
            
            # Render email template
            html_message = render_to_string('emails/contact_notification.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email using settings from settings.py
            send_mail(
                subject=f'New Contact Form Submission: {contact.get_purpose_display()}',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'address': '123 Tech Street, Kathmandu, Nepal',
        'phone': '+977 1234567890',
        'email': 'contact@sipalayainfotech.com',
        'google_maps_embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.4643173158867!2d85.31727761509467!3d27.709240982784!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb1907b05d4f6f%3A0x60456a3a5b33d300!2sKathmandu%2C%20Nepal!5e0!3m2!1sen!2s!4v1647881234567!5m2!1sen!2s',
        'social_links': {
            'facebook': 'https://facebook.com/sipalayainfotech',
            'linkedin': 'https://linkedin.com/company/sipalayainfotech',
            'instagram': 'https://instagram.com/sipalayainfotech',
        }
    }
    return render(request, 'contact.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')
