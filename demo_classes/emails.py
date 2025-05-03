from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)

def send_booking_confirmation(booking):
    """Send booking confirmation email to student"""
    try:
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise ImproperlyConfigured("Email settings are not properly configured")
            
        subject = f'Demo Class Booking Confirmation - {booking.schedule.demo_class.title}'
        current_site = Site.objects.get_current()
        context = {
            'booking': booking,
            'demo_class': booking.schedule.demo_class,
            'schedule': booking.schedule,
            'site': current_site,
            'booking_url': f'https://{current_site.domain}{reverse("demo_classes:my_bookings")}'
        }
        message = render_to_string('demo_classes/emails/booking_confirmation.txt', context)
        html_message = render_to_string('demo_classes/emails/booking_confirmation.html', context)
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Booking confirmation email sent to {booking.user.email}")
    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {str(e)}")
        raise

def send_booking_cancellation(booking):
    """Send booking cancellation email to student"""
    subject = f'Demo Class Booking Cancelled - {booking.schedule.demo_class.title}'
    context = {
        'booking': booking,
        'demo_class': booking.schedule.demo_class,
        'schedule': booking.schedule,
    }
    message = render_to_string('demo_classes/emails/booking_cancellation.txt', context)
    html_message = render_to_string('demo_classes/emails/booking_cancellation.html', context)
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.user.email],
        html_message=html_message,
    )

def send_reminder(booking):
    """Send reminder email before demo class"""
    subject = f'Reminder: Demo Class Tomorrow - {booking.schedule.demo_class.title}'
    context = {
        'booking': booking,
        'demo_class': booking.schedule.demo_class,
        'schedule': booking.schedule,
    }
    message = render_to_string('demo_classes/emails/reminder.txt', context)
    html_message = render_to_string('demo_classes/emails/reminder.html', context)
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.user.email],
        html_message=html_message,
    ) 