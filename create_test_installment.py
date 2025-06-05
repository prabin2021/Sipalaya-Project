import os
import django
from datetime import datetime, timedelta
from django.utils import timezone
import uuid
from django.conf import settings
from django.db import transaction

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipalaya_tech.settings')
django.setup()

from courses.models import Payment, Course, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_installment():
    # Get or create a test user with a unique username
    username = f'testuser_{uuid.uuid4().hex[:8]}'
    test_user, created = User.objects.get_or_create(
        email='sigdelprabin321@gmail.com',  # The email where you want to receive the warning
        defaults={
            'username': username,
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )
    
    # Get the first course
    course = Course.objects.first()
    if not course:
        print("No courses found in the database. Please create a course first.")
        return
    
    with transaction.atomic():
        # Create an installment payment
        payment = Payment.objects.create(
            student=test_user,
            course=course,
            amount=course.price / 3,  # Split into 3 installments
            payment_type='installment',
            status='completed',
            total_installments=3,
            current_installment=1,
            transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}"
        )
        
        # Set the next_installment_due to 2 days ago
        overdue_date = timezone.now() - timedelta(days=2)
        payment.next_installment_due = overdue_date
        payment.save(update_fields=['next_installment_due'])
        
        # Create enrollment
        enrollment, created = Enrollment.objects.get_or_create(
            student=test_user,
            course=course,
            defaults={'payment': payment}
        )
    
    print(f"Created test installment payment:")
    print(f"Student: {test_user.email}")
    print(f"Course: {course.title}")
    print(f"Amount: {payment.amount}")
    print(f"Installment: {payment.current_installment} of {payment.total_installments}")
    print(f"Due Date: {payment.next_installment_due}")
    print(f"Current time: {timezone.now()}")
    print(f"Is overdue: {payment.is_installment_overdue()}")
    print("\nNow run: python manage.py check_installments")

if __name__ == '__main__':
    create_test_installment() 