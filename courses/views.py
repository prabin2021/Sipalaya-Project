from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import requests
from .models import (
    Course, Category, Enrollment, Module, 
    Lesson, Assignment, Submission, DemoClass, 
    DemoClassBooking, Payment, Invoice,
    LessonProgress, Certificate, Review
)
from instructor.models import InstructorProfile
import uuid
from django.db import models

def course_list(request):
    categories = Category.objects.all()
    courses = Course.objects.all()
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Filtering
    category = request.GET.get('category')
    level = request.GET.get('level')
    duration = request.GET.get('duration')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if category:
        courses = courses.filter(category__slug=category)
    if level:
        courses = courses.filter(level=level)
    if duration:
        courses = courses.filter(duration=duration)
    if price_min:
        courses = courses.filter(price__gte=price_min)
    if price_max:
        courses = courses.filter(price__lte=price_max)
    
    # Sorting
    sort = request.GET.get('sort')
    if sort == 'popularity':
        # Annotate with enrollment count and sort
        courses = courses.annotate(
            enrollment_count=models.Count('enrollments')
        ).order_by('-enrollment_count')
    elif sort == 'newest':
        courses = courses.order_by('-created_at')
    elif sort == 'price_asc':
        courses = courses.order_by('price')
    elif sort == 'price_desc':
        courses = courses.order_by('-price')
    
    context = {
        'categories': categories,
        'courses': courses,
        'current_category': category,
        'current_level': level,
        'current_duration': duration,
        'current_sort': sort,
        'price_min': price_min,
        'price_max': price_max,
        'search_query': search_query,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        # Redirect enrolled students to course content
        if is_enrolled:
            return redirect('student:course_content', slug=slug)
    
    # Get upcoming demo classes
    demo_classes = DemoClass.objects.filter(
        course=course,
        is_active=True,
        date__gte=timezone.now().date()
    ).order_by('date', 'time')
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'demo_classes': demo_classes,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, f'You are already enrolled in {course.title}')
        return redirect('courses:course_detail', slug=slug)
    
    # Check if payment exists and is completed
    payment = Payment.objects.filter(
        student=request.user,
        course=course,
        status='completed'
    ).first()
    
    if not payment:
        # Redirect to payment page
        return render(request, 'courses/payment_options.html', {
            'course': course,
            'payment_types': [
                ('full', 'Full Payment'),
                ('installment', 'Installment Payment')
            ]
        })
    
    # Create enrollment with payment
    enrollment = Enrollment.objects.create(
        student=request.user,
        course=course,
        payment=payment
    )
    
    messages.success(request, f'Successfully enrolled in {course.title}')
    return redirect('courses:course_detail', slug=slug)

@login_required
def course_content(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    modules = course.modules.all()
    
    return render(request, 'courses/course_content.html', {
        'course': course,
        'enrollment': enrollment,
        'modules': modules
    })

@login_required
def lesson_detail(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment
    })

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        comments = request.POST.get('comments', '')
        file = request.FILES.get('file')
        
        submission, created = Submission.objects.get_or_create(
            assignment=assignment,
            student=request.user,
            defaults={
                'content': comments,
                'file': file,
                'status': 'pending'
            }
        )
        
        if not created:
            submission.content = comments
            if file:
                submission.file = file
            submission.status = 'pending'
            submission.save()
        
        messages.success(request, 'Assignment submitted successfully')
        return redirect('student:dashboard')
    
    return render(request, 'courses/submit_assignment.html', {
        'assignment': assignment,
        'now': timezone.now()
    })

@login_required
def book_demo_class(request, demo_class_id):
    demo_class = get_object_or_404(DemoClass, id=demo_class_id, is_active=True)
    
    if demo_class.current_participants >= demo_class.max_participants:
        messages.error(request, 'Sorry, this demo class is full.')
        return redirect('courses:course_detail', slug=demo_class.course.slug)
    
    # Check if user already booked
    if DemoClassBooking.objects.filter(demo_class=demo_class, student=request.user).exists():
        messages.warning(request, 'You have already booked this demo class.')
        return redirect('courses:course_detail', slug=demo_class.course.slug)
    
    # Create booking
    DemoClassBooking.objects.create(demo_class=demo_class, student=request.user)
    demo_class.current_participants += 1
    demo_class.save()
    
    messages.success(request, 'Demo class booked successfully!')
    return redirect('courses:course_detail', slug=demo_class.course.slug)

@login_required
def initiate_payment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    payment_type = request.POST.get('payment_type', 'full')
    installments = int(request.POST.get('installments', 1))
    
    # Calculate payment amount
    if payment_type == 'full':
        amount = float(course.price)
        total_installments = 1
    else:
        # Add 10% interest for installment payments
        total_amount = float(course.price) * 1.1
        amount = total_amount / installments
        total_installments = installments
    
    # Generate a unique transaction ID
    transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    
    # Create payment record
    payment = Payment.objects.create(
        student=request.user,
        course=course,
        amount=amount,
        payment_type=payment_type,
        total_installments=total_installments,
        transaction_id=transaction_id
    )
    
    # Generate invoice
    invoice = Invoice.objects.create(
        student=request.user,
        amount=amount,
        payment=payment
    )
    
    # Prepare Khalti payment data
    import requests
    import json
    
    # Convert amount to paisa (Khalti uses paisa as the smallest unit)
    amount_in_paisa = int(amount * 100)
    
    # Ensure minimum amount of 1000 paisa (Rs. 10)
    if amount_in_paisa < 1000:
        amount_in_paisa = 1000
    
    # Prepare the payload for Khalti
    payload = {
        "return_url": request.build_absolute_uri(reverse('courses:payment_success')),
        "website_url": request.build_absolute_uri('/'),
        "amount": amount_in_paisa,
        "purchase_order_id": str(payment.id),
        "purchase_order_name": f"Course: {course.title}",
        "customer_info": {
            "name": request.user.get_full_name() or request.user.email,
            "email": request.user.email,
            "phone": request.user.phone if hasattr(request.user, 'phone') else ""
        }
    }
    
    # Headers for Khalti API
    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        # Debug prints
        print("\nDebug - Khalti API Request:")
        print(f"URL: {settings.KHALTI_INITIATE_URL}")
        print(f"Headers: {headers}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Make request to Khalti
        response = requests.post(
            settings.KHALTI_INITIATE_URL,
            json=payload,
            headers=headers
        )
        
        # Debug prints
        print("\nDebug - Khalti API Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            payment_data = response.json()
            
            # Update payment record with Khalti reference
            payment.khalti_payment_id = payment_data.get('pidx')
            payment.save()
            
            # Return the payment URL to redirect the user
            return render(request, 'courses/payment_redirect.html', {
                'payment_url': payment_data.get('payment_url'),
                'amount': amount,
                'course': course
            })
        else:
            error_message = "Failed to initiate payment. "
            try:
                error_data = response.json()
                error_message += error_data.get('detail', 'Please try again.')
            except:
                error_message += "Please try again."
            
            messages.error(request, error_message)
            return redirect('courses:course_detail', slug=slug)
            
    except requests.RequestException as e:
        print(f"\nDebug - Request Exception: {str(e)}")
        messages.error(request, 'Error connecting to payment gateway. Please try again.')
        return redirect('courses:course_detail', slug=slug)

@login_required
def payment_success(request):
    pidx = request.GET.get('pidx')
    transaction_id = request.GET.get('transaction_id')
    status = request.GET.get('status')
    
    if not pidx or not transaction_id:
        messages.error(request, 'Invalid payment response.')
        return redirect('course_list')
    
    try:
        # Verify payment with Khalti
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        
        response = requests.post(
            settings.KHALTI_VERIFICATION_URL,
            json={"pidx": pidx},
            headers=headers
        )
        
        # Debug prints
        print("\nDebug - Khalti Verification Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            verification_data = response.json()
            
            if verification_data.get('status') == 'Completed':
                # Update payment status
                payment = Payment.objects.get(khalti_payment_id=pidx)
                payment.status = 'completed'
                payment.khalti_transaction_id = transaction_id
                
                # If this is an installment payment, increment the current installment
                if payment.payment_type == 'installment':
                    payment.current_installment += 1
                    # Set next installment due date to 30 days from now
                    payment.next_installment_due = timezone.now() + timezone.timedelta(days=30)
                
                payment.save()
                
                # Create or update enrollment
                enrollment, created = Enrollment.objects.get_or_create(
                    student=payment.student,
                    course=payment.course,
                    defaults={'payment': payment}
                )
                
                if not created:
                    enrollment.payment = payment
                    enrollment.save()
                
                messages.success(request, 'Payment successful! You are now enrolled in the course.')
                return redirect('courses:course_detail', slug=payment.course.slug)
            
        messages.error(request, 'Payment verification failed.')
        return redirect('payment_failed')
        
    except Payment.DoesNotExist:
        messages.error(request, 'Payment record not found.')
    except requests.RequestException:
        messages.error(request, 'Error verifying payment. Please contact support.')
    
    return redirect('payment_failed')

@login_required
def payment_failed(request):
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('courses:course_list')

@login_required
def student_dashboard(request):
    # Get enrolled courses
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    # Calculate progress for each course
    for enrollment in enrollments:
        total_lessons = Lesson.objects.filter(module__course=enrollment.course).count()
        completed_lessons = 0  # We'll implement this later
        enrollment.progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    # Get recent assignments
    recent_assignments = Assignment.objects.filter(
        lesson__module__course__enrollments__student=request.user
    ).select_related('lesson', 'lesson__module', 'lesson__module__course').order_by('-due_date')[:5]
    
    # Get upcoming assignments
    upcoming_assignments = Assignment.objects.filter(
        lesson__module__course__enrollments__student=request.user,
        due_date__gt=timezone.now()
    ).select_related('lesson', 'lesson__module', 'lesson__module__course').order_by('due_date')[:5]
    
    # Get attendance records
    attendance_records = DemoClassBooking.objects.filter(
        student=request.user,
        demo_class__date__gte=timezone.now().date() - timezone.timedelta(days=30)
    ).select_related('demo_class', 'demo_class__course').order_by('-demo_class__date')
    
    context = {
        'enrollments': enrollments,
        'recent_assignments': recent_assignments,
        'upcoming_assignments': upcoming_assignments,
        'attendance_records': attendance_records,
    }
    return render(request, 'courses/student_dashboard.html', context)

@login_required
def course_progress(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    # Get all modules and lessons
    modules = Module.objects.filter(course=course).prefetch_related('lessons')
    
    # Get completed lessons (we'll implement this later)
    completed_lessons = set()  # This will be populated from a model we'll create
    
    # Calculate progress
    total_lessons = sum(module.lessons.count() for module in modules)
    completed_count = len(completed_lessons)
    progress_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'modules': modules,
        'completed_lessons': completed_lessons,
        'progress_percentage': progress_percentage,
        'total_lessons': total_lessons,
        'completed_count': completed_count,
    }
    return render(request, 'courses/course_progress.html', context)

@login_required
def installment_payments(request):
    """View for displaying and managing installment payments."""
    # Get all installment payments for the user
    installment_payments = Payment.objects.filter(
        student=request.user,
        payment_type='installment'
    ).select_related('course')
    
    # Check and update completion status for all payments
    for payment in installment_payments:
        payment.check_installment_completion()
    
    # Filter active installments (where current_installment < total_installments)
    active_installments = installment_payments.filter(
        status='completed',
        current_installment__lt=models.F('total_installments')
    )
    
    # Get pending installments
    pending_installments = installment_payments.filter(
        status='pending'
    )
    
    # Get completed installments
    completed_installments = installment_payments.filter(
        status='completed',
        current_installment=models.F('total_installments')
    )
    
    context = {
        'active_installments': active_installments,
        'pending_installments': pending_installments,
        'completed_installments': completed_installments,
    }
    return render(request, 'courses/installment_payments.html', context)

@login_required
def pay_installment(request, payment_id):
    """View for processing installment payments."""
    payment = get_object_or_404(Payment, id=payment_id, student=request.user)
    
    if not payment.can_pay_next_installment():
        messages.error(request, 'This installment cannot be paid at this time.')
        return redirect('installment_payments')
    
    # Calculate next installment amount
    amount = payment.get_next_installment_amount()
    
    # Prepare Khalti payment data
    amount_in_paisa = int(amount * 100)
    
    # Ensure minimum amount of 1000 paisa (Rs. 10)
    if amount_in_paisa < 1000:
        amount_in_paisa = 1000
    
    # Prepare the payload for Khalti
    payload = {
        "return_url": request.build_absolute_uri(reverse('courses:payment_success')),
        "website_url": request.build_absolute_uri('/'),
        "amount": amount_in_paisa,
        "purchase_order_id": str(payment.id),
        "purchase_order_name": f"Installment {payment.installment_number + 1} for {payment.course.title}",
        "customer_info": {
            "name": request.user.get_full_name() or request.user.email,
            "email": request.user.email,
            "phone": request.user.phone if hasattr(request.user, 'phone') else ""
        }
    }
    
    # Headers for Khalti API
    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(
            settings.KHALTI_INITIATE_URL,
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            payment_data = response.json()
            
            # Update payment record with Khalti reference
            payment.khalti_payment_id = payment_data.get('pidx')
            payment.save()
            
            # Return the payment URL to redirect the user
            return render(request, 'courses/payment_redirect.html', {
                'payment_url': payment_data.get('payment_url'),
                'amount': amount,
                'course': payment.course,
                'is_installment': True
            })
        else:
            messages.error(request, 'Failed to initiate payment. Please try again.')
            return redirect('installment_payments')
            
    except requests.RequestException:
        messages.error(request, 'Error connecting to payment gateway. Please try again.')
        return redirect('installment_payments')

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        video_url = request.POST.get('video_url')
        is_video = bool(video_url)
        
        testimonial = Testimonial.objects.create(
            student=request.user,
            content=content,
            video_url=video_url,
            is_video=is_video
        )
        messages.success(request, 'Your testimonial has been submitted for review.')
        return redirect('courses:testimonials')
    
    return render(request, 'courses/testimonial_form.html')

@login_required
def add_review(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    # Check if user is enrolled in the course
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled in the course to leave a review.')
        return redirect('courses:course_detail', slug=slug)
    
    # Check if user has already reviewed
    existing_review = Review.objects.filter(student=request.user, course=course).first()
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if existing_review:
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
            messages.success(request, 'Your review has been updated.')
        else:
            Review.objects.create(
                student=request.user,
                course=course,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Your review has been submitted for review.')
        
        return redirect('courses:course_detail', slug=slug)
    
    return render(request, 'courses/add_review.html', {
        'course': course,
        'existing_review': existing_review
    })

def testimonials(request):
    testimonials = Testimonial.objects.filter(is_approved=True)
    return render(request, 'courses/testimonials.html', {
        'testimonials': testimonials
    })