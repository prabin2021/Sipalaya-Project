import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipalaya_tech.settings')
django.setup()

from courses.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

def update_installment():
    # Get the user's payment
    payment = Payment.objects.filter(
        student__email='sigdelprabin321@gmail.com',
        payment_type='installment',
        status='completed'
    ).first()
    
    if not payment:
        print("No payment found for sigdelprabin321@gmail.com")
        return
    
    # Set next installment due to 30 days from now
    payment.next_installment_due = timezone.now() + timedelta(days=30)
    payment.save()
    
    print(f"\nUpdated payment:")
    print(f"Course: {payment.course.title}")
    print(f"Current Installment: {payment.current_installment} of {payment.total_installments}")
    print(f"Next Due Date: {payment.next_installment_due}")

if __name__ == '__main__':
    update_installment() 