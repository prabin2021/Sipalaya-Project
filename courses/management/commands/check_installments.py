from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.db import models
from courses.models import Payment, Enrollment
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check for overdue installments and send warning emails'

    def handle(self, *args, **options):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger.info("Starting check_installments command...")
        
        # Get all active installment payments
        active_payments = Payment.objects.filter(
            payment_type='installment',
            status='completed',
            installment_number__lt=models.F('total_installments')
        ).select_related('student', 'course')
        
        logger.info(f"Found {active_payments.count()} active installment payments")
        
        for payment in active_payments:
            logger.info(f"Checking payment for student {payment.student.email} - Course: {payment.course.title}")
            
            if payment.is_installment_overdue():
                logger.info(f"Payment is overdue. Next installment due: {payment.next_installment_due}")
                
                # Check if we've already sent a warning in the last 24 hours
                if not payment.last_warning_sent or \
                   timezone.now() - payment.last_warning_sent > timedelta(days=settings.INSTALLMENT_WARNING_INTERVAL):
                    
                    logger.info("Sending warning email...")
                    
                    # Send warning email
                    subject = f'Urgent: Overdue Installment Payment for {payment.course.title}'
                    message = f"""
                    Dear {payment.student.get_full_name() or payment.student.email},

                    This is an urgent reminder that your installment payment for {payment.course.title} is overdue.

                    Payment Details:
                    - Course: {payment.course.title}
                    - Installment: {payment.installment_number} of {payment.total_installments}
                    - Amount Due: Rs. {payment.amount}
                    - Due Date: {payment.next_installment_due.strftime('%B %d, %Y')}

                    Important: You have {settings.INSTALLMENT_WARNING_DAYS} days to make this payment to avoid being removed from the course.

                    To make your payment:
                    1. Log in to your account
                    2. Go to Installment Payments
                    3. Click "Pay Now" for the overdue installment

                    If you have any questions or need assistance, please contact our support team immediately.

                    Best regards,
                    Sipalaya Info Tech Team
                    """
                    
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [payment.student.email],
                            fail_silently=False,
                        )
                        
                        # Update last warning sent timestamp
                        payment.last_warning_sent = timezone.now()
                        payment.save()
                        
                        logger.info(f"Warning email sent successfully to {payment.student.email}")
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Warning email sent to {payment.student.email} for {payment.course.title}'
                            )
                        )
                    except Exception as e:
                        logger.error(f"Failed to send warning email: {str(e)}")
                        self.stdout.write(
                            self.style.ERROR(
                                f'Failed to send warning email to {payment.student.email}: {str(e)}'
                            )
                        )
                else:
                    logger.info(f"Warning email already sent at {payment.last_warning_sent}")
                
                # If payment is overdue by more than INSTALLMENT_WARNING_DAYS, remove student from course
                if timezone.now() - payment.next_installment_due > timedelta(days=settings.INSTALLMENT_WARNING_DAYS):
                    logger.info("Payment is overdue by more than warning days, removing course access...")
                    try:
                        # Get the enrollment and mark it as incomplete
                        enrollment = Enrollment.objects.get(
                            student=payment.student,
                            course=payment.course
                        )
                        enrollment.completed = False
                        enrollment.save()
                        
                        # Send final notification email
                        subject = f'Course Access Removed: {payment.course.title}'
                        message = f"""
                        Dear {payment.student.get_full_name() or payment.student.email},

                        We regret to inform you that your access to {payment.course.title} has been removed
                        due to non-payment of the overdue installment.

                        Payment Details:
                        - Course: {payment.course.title}
                        - Installment: {payment.installment_number} of {payment.total_installments}
                        - Amount Due: Rs. {payment.amount}
                        - Due Date: {payment.next_installment_due.strftime('%B %d, %Y')}

                        To regain access to the course:
                        1. Contact our support team immediately
                        2. Make the overdue payment
                        3. We will restore your access within 24 hours of payment confirmation

                        If you believe this is an error or have any questions, please contact our support team.

                        Best regards,
                        Sipalaya Info Tech Team
                        """
                        
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [payment.student.email],
                            fail_silently=False,
                        )
                        
                        logger.info(f"Course access removed for {payment.student.email}")
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Removed course access for {payment.student.email} from {payment.course.title}'
                            )
                        )
                    except Exception as e:
                        logger.error(f"Failed to remove course access: {str(e)}")
                        self.stdout.write(
                            self.style.ERROR(
                                f'Failed to remove course access for {payment.student.email}: {str(e)}'
                            )
                        )
            else:
                logger.info("Payment is not overdue") 