from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
import stripe
from .models import Payment, Refund, Coupon
from courses.models import Course, Enrollment

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = 'payments/payment_form.html'
    fields = ['payment_method']
    
    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        form.instance.student = self.request.user
        form.instance.course = course
        form.instance.amount = course.price
        
        # Apply coupon if provided
        coupon_code = self.request.POST.get('coupon')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                form.instance.amount = form.instance.amount * (1 - coupon.discount_percentage / 100)
            except Coupon.DoesNotExist:
                messages.error(self.request, 'Invalid coupon code!')
                return self.form_invalid(form)
        
        # Create Stripe payment intent
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(form.instance.amount * 100),  # Convert to cents
                currency='usd',
                metadata={'course_id': course.id, 'student_id': self.request.user.id}
            )
            form.instance.transaction_id = intent.id
            messages.success(self.request, 'Payment processed successfully!')
            return super().form_valid(form)
        except stripe.error.StripeError as e:
            messages.error(self.request, f'Payment failed: {str(e)}')
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'slug': self.kwargs['slug']})

class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    
    def get_queryset(self):
        return Payment.objects.filter(student=self.request.user).order_by('-created_at')

class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'
    
    def get_queryset(self):
        return Payment.objects.filter(student=self.request.user)

class RefundCreateView(LoginRequiredMixin, CreateView):
    model = Refund
    template_name = 'payments/refund_form.html'
    fields = ['reason']
    
    def form_valid(self, form):
        payment = get_object_or_404(Payment, id=self.kwargs['payment_id'])
        if payment.student != self.request.user:
            messages.error(self.request, 'You are not authorized to request a refund for this payment!')
            return self.form_invalid(form)
        
        form.instance.payment = payment
        form.instance.amount = payment.amount
        messages.success(self.request, 'Refund request submitted successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('payments:payment_detail', kwargs={'pk': self.kwargs['payment_id']})

class RefundListView(LoginRequiredMixin, ListView):
    model = Refund
    template_name = 'payments/refund_list.html'
    context_object_name = 'refunds'
    
    def get_queryset(self):
        return Refund.objects.filter(payment__student=self.request.user).order_by('-created_at') 