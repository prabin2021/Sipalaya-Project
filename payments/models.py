from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from courses.models import Course

class Payment(models.Model):
    """Payment model."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('CREDIT_CARD', _('Credit Card')),
            ('DEBIT_CARD', _('Debit Card')),
            ('PAYPAL', _('PayPal')),
            ('BANK_TRANSFER', _('Bank Transfer')),
        ]
    )
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', _('Pending')),
            ('COMPLETED', _('Completed')),
            ('FAILED', _('Failed')),
            ('REFUNDED', _('Refunded')),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.student.email}"

class Refund(models.Model):
    """Refund model."""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', _('Pending')),
            ('APPROVED', _('Approved')),
            ('REJECTED', _('Rejected')),
            ('COMPLETED', _('Completed')),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('refund')
        verbose_name_plural = _('refunds')
    
    def __str__(self):
        return f"Refund for Payment {self.payment.transaction_id}"

class Coupon(models.Model):
    """Coupon model."""
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('coupon')
        verbose_name_plural = _('coupons')
    
    def __str__(self):
        return self.code 