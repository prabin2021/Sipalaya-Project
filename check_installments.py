import os
import django
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipalaya_tech.settings')
django.setup()

from courses.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

def check_pending_installments():
    # Get the user
    user = User.objects.filter(email='sigdelprabin321@gmail.com').first()
    
    if not user:
        print("User not found with email: sigdelprabin321@gmail.com")
        return
    
    # Get all installment payments
    payments = Payment.objects.filter(
        student=user,
        payment_type='installment'
    ).select_related('course')
    
    print(f"\nFound {payments.count()} installment payments for {user.email}")
    
    for payment in payments:
        print(f"\nPayment ID: {payment.id}")
        print(f"Course: {payment.course.title if payment.course else 'No course'}")
        print(f"Amount: {payment.amount}")
        print(f"Status: {payment.status}")
        print(f"Current Installment: {payment.current_installment}")
        print(f"Total Installments: {payment.total_installments}")
        print(f"Next Due Date: {payment.next_installment_due}")
        print(f"Can pay next installment: {payment.can_pay_next_installment()}")
        print(f"Is overdue: {payment.is_installment_overdue()}")

if __name__ == '__main__':
    check_pending_installments() 