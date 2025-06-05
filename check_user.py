import os
import django
from django.utils import timezone
from django.db.models import F

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipalaya_tech.settings')
django.setup()

from courses.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

def check_user_installments():
    # Get the user
    user = User.objects.filter(email='sigdelprabin321@gmail.com').first()
    
    if not user:
        print("User not found with email: sigdelprabin321@gmail.com")
        return
    
    # Check pending installments
    pending_installments = Payment.objects.filter(
        student=user,
        payment_type='installment',
        status='completed'
    ).filter(
        current_installment__lt=F('total_installments')
    )
    
    print(f"\nUser: {user.email}")
    print(f"Has pending installments: {pending_installments.exists()}")
    
    for payment in pending_installments:
        print(f"\nPayment Details:")
        print(f"Course: {payment.course.title if payment.course else 'No course'}")
        print(f"Current Installment: {payment.current_installment}")
        print(f"Total Installments: {payment.total_installments}")
        print(f"Status: {payment.status}")
        print(f"Payment Type: {payment.payment_type}")

if __name__ == '__main__':
    check_user_installments() 