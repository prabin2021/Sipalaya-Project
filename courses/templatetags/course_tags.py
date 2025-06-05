from django import template
from django.db.models import F, Q
from courses.models import Payment
import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.simple_tag
def has_pending_installments(user):
    """Check if the user has any pending payments or incomplete installments."""
    logger.info(f"Checking pending installments for user: {user.email}")
    
    # Get all payments for the user
    payments = Payment.objects.filter(student=user)
    logger.info(f"Found {payments.count()} total payments")
    
    # Check for pending payments
    pending_payments = payments.filter(status='pending')
    logger.info(f"Found {pending_payments.count()} pending payments")
    
    # Check for incomplete installments
    incomplete_installments = payments.filter(
        payment_type='installment',
        current_installment__lt=F('total_installments')
    )
    logger.info(f"Found {incomplete_installments.count()} incomplete installments")
    
    # Check if any payments match our criteria
    has_pending = (pending_payments | incomplete_installments).exists()
    logger.info(f"Has pending installments: {has_pending}")
    
    return has_pending 