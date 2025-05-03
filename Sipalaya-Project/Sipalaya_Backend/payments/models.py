from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.utils import timezone

class PaymentMethod(models.Model):
    PAYMENT_TYPES = [
        ('stripe', 'Stripe'),
        ('khalti', 'Khalti'),
    ]
    
    name = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    is_active = models.BooleanField(default=True)
    api_key = models.CharField(max_length=255, blank=True)
    secret_key = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For installment payments
    is_installment = models.BooleanField(default=False)
    installment_number = models.PositiveIntegerField(null=True, blank=True)
    total_installments = models.PositiveIntegerField(null=True, blank=True)
    
    # For refunds
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    refund_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.student.get_full_name()}"

    class Meta:
        ordering = ['-created_at']

class InstallmentPlan(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_installments = models.PositiveIntegerField()
    amount_per_installment = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Installment Plan - {self.student.get_full_name()} - {self.course.title}"

    def calculate_remaining_amount(self):
        paid_amount = sum(payment.amount for payment in self.payment_set.filter(status='completed'))
        return self.total_amount - paid_amount

    def get_next_installment_date(self):
        if not self.payment_set.exists():
            return self.start_date
        last_payment = self.payment_set.order_by('-payment_date').first()
        if last_payment:
            return last_payment.payment_date + timezone.timedelta(days=30)
        return self.start_date
