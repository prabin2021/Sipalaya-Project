import os
import django
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipalaya_tech.settings')
django.setup()

def test_email():
    try:
        # Print current email settings
        print("Current email settings:")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        
        # Try sending email using Django's send_mail
        print("\nTrying to send email using Django's send_mail...")
        send_mail(
            'Test Email from Django',
            'This is a test email to verify SMTP settings.',
            settings.EMAIL_HOST_USER,
            ['sigdelprabin321@gmail.com'],
            fail_silently=False,
        )
        print("Test email sent successfully!")
        
    except Exception as e:
        print(f"\nFailed to send email. Error: {str(e)}")
        print("\nTrying direct SMTP connection...")
        try:
            # Try direct SMTP connection
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = 'sigdelprabin321@gmail.com'
            msg['Subject'] = 'Test Email via Direct SMTP'
            
            body = 'This is a test email sent via direct SMTP connection.'
            msg.attach(MIMEText(body, 'plain'))
            
            server.send_message(msg)
            server.quit()
            print("Direct SMTP test email sent successfully!")
            
        except Exception as smtp_error:
            print(f"Direct SMTP connection failed. Error: {str(smtp_error)}")

if __name__ == '__main__':
    test_email() 