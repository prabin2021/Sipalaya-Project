from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
import uuid
import logging

# Import models
from .models import Payment, PaymentMethod, InstallmentPlan
from courses.models import Course, Enrollment

# Configure logging
logger = logging.getLogger('payments')

@login_required
def initiate_payment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        is_installment = request.POST.get('is_installment') == 'true'
        
        try:
            payment_method_obj = PaymentMethod.objects.get(name=payment_method)
        except PaymentMethod.DoesNotExist:
            messages.error(request, "Invalid payment method selected.")
            return redirect('payments:initiate_payment', course_id=course.id)
        
        if is_installment:
            number_of_installments = int(request.POST.get('number_of_installments', 3))
            amount_per_installment = course.price / number_of_installments
            
            # Create installment plan
            installment_plan = InstallmentPlan.objects.create(
                student=request.user,
                course=course,
                total_amount=course.price,
                number_of_installments=number_of_installments,
                amount_per_installment=amount_per_installment,
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timezone.timedelta(days=30 * number_of_installments)
            )
            
            # Create first payment
            payment = Payment.objects.create(
                student=request.user,
                course=course,
                amount=amount_per_installment,
                payment_method=payment_method_obj,
                transaction_id=str(uuid.uuid4()),
                is_installment=True,
                installment_number=1,
                total_installments=number_of_installments
            )
        else:
            # Full payment
            payment = Payment.objects.create(
                student=request.user,
                course=course,
                amount=course.price,
                payment_method=payment_method_obj,
                transaction_id=str(uuid.uuid4())
            )
        
        messages.error(request, "Payment processor not implemented yet.")
        return redirect('courses:course_detail', course_id=course.id)
    
    return render(request, 'payments/payment_method.html', {
        'course': course,
        'payment_methods': payment_methods
    })

@login_required
def payment_history(request):
    payments = Payment.objects.filter(student=request.user).order_by('-created_at')
    installment_plans = InstallmentPlan.objects.filter(student=request.user, is_active=True)
    
    return render(request, 'payments/payment_history.html', {
        'payments': payments,
        'installment_plans': installment_plans
    })

@login_required
def installment_details(request, plan_id):
    installment_plan = get_object_or_404(InstallmentPlan, id=plan_id, student=request.user)
    payments = Payment.objects.filter(
        student=request.user,
        course=installment_plan.course,
        is_installment=True
    ).order_by('installment_number')
    
    return render(request, 'payments/installment_details.html', {
        'plan': installment_plan,
        'payments': payments,
        'remaining_balance': installment_plan.total_amount - sum(p.amount for p in payments)
    })