import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Course, Category, DemoClass, DemoClassRegistration, Payment, Enrollment, CourseResource
from .forms import ResourceUploadForm
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
import time
from django.urls import reverse
import hmac
import hashlib
import base64
import uuid

def course_list(request):
    # Start with base queryset
    courses = Course.objects.filter(is_active=True).select_related('instructor', 'category')
    
    # Get filter parameters
    skill_level = request.GET.get('skill_level')
    duration = request.GET.get('duration')
    price_range = request.GET.get('price_range')
    sort = request.GET.get('sort', 'popularity')
    
    # Apply filters using Q objects for better query optimization
    filters = Q()
    
    if skill_level:
        filters &= Q(skill_level=skill_level)
    
    if duration:
        if duration == 'short':
            filters &= Q(duration__lte=3)
        elif duration == 'medium':
            filters &= Q(duration__gt=3, duration__lte=6)
        elif duration == 'long':
            filters &= Q(duration__gt=6)
    
    if price_range:
        if price_range == 'low':
            filters &= Q(price__lt=20000)
        elif price_range == 'medium':
            filters &= Q(price__gte=20000, price__lte=50000)
        elif price_range == 'high':
            filters &= Q(price__gt=50000)
    
    # Apply the filters
    courses = courses.filter(filters)
    
    # Apply sorting with proper indexing
    sort_options = {
        'popularity': '-enrollment_count',
        'newest': '-created_at',
        'price_low': 'price',
        'price_high': '-price',
        'rating': '-rating',
        'duration': 'duration'
    }
    
    sort_field = sort_options.get(sort, '-enrollment_count')
    courses = courses.order_by(sort_field)
    
    # Get total count for pagination
    total_courses = courses.count()
    
    # Prepare context with all necessary data
    context = {
        'courses': courses,
        'total_courses': total_courses,
        'current_filters': {
            'skill_level': skill_level,
            'duration': duration,
            'price_range': price_range,
            'sort': sort
        },
        'filter_options': {
            'skill_levels': Course.SKILL_LEVELS,
            'durations': Course.DURATION_CHOICES,
            'price_ranges': [
                ('low', 'Under Rs. 20,000'),
                ('medium', 'Rs. 20,000 - 50,000'),
                ('high', 'Over Rs. 50,000')
            ],
            'sort_options': [
                ('popularity', 'Most Popular'),
                ('newest', 'Newest First'),
                ('price_low', 'Price: Low to High'),
                ('price_high', 'Price: High to Low'),
                ('rating', 'Highest Rated'),
                ('duration', 'Duration')
            ]
        }
    }
    
    return render(request, 'courses/course_list.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    syllabus_items = course.syllabus.split("\n")
    prerequisites = course.prerequisites.split("\n")
    return render(request, 'courses/course_detail.html', {'course': course, 'syllabus_items': syllabus_items, 'prerequisites': prerequisites,})

def courses_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/course_list.html', {'courses': courses, 'category': category})

def search_courses(request):
    query = request.GET.get('q', '')
    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).filter(is_active=True)
    else:
        courses = Course.objects.filter(is_active=True)
    
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def demo_class_schedule(request, course_id=None):
    if course_id:
        course = get_object_or_404(Course, id=course_id, is_active=True)
        demo_classes = DemoClass.objects.filter(
            course=course,
            is_active=True,
            date__gte=timezone.now().date()
        )
    else:
        course = None
        demo_classes = DemoClass.objects.filter(
            is_active=True,
            date__gte=timezone.now().date()
        )
    
    return render(request, 'courses/demo_class.html', {
        'course': course,
        'demo_classes': demo_classes
    })

@login_required
def register_demo_class(request, demo_class_id):
    demo_class = get_object_or_404(DemoClass, id=demo_class_id, is_active=True)
    
    if demo_class.current_students >= demo_class.max_students:
        messages.error(request, 'Sorry, this demo class is full.')
        return redirect('demo_class_schedule', course_id=demo_class.course.id)
    
    # Check if student is already registered
    if DemoClassRegistration.objects.filter(demo_class=demo_class, student=request.user).exists():
        messages.error(request, 'You are already registered for this demo class.')
        return redirect('demo_class_schedule', course_id=demo_class.course.id)
    
    # Create registration
    DemoClassRegistration.objects.create(
        demo_class=demo_class,
        student=request.user
    )
    
    # Update current students count
    demo_class.current_students += 1
    demo_class.save()
    
    messages.success(request, 'Successfully registered for the demo class!')
    return redirect('demo_class_schedule', course_id=demo_class.course.id)

@login_required
def payment_page(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        return render(request, 'courses/payment.html', {'course': course})
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_list')

@login_required
def process_payment(request, course_id):
    if request.method != 'POST':
        return redirect('payment_page', course_id=course_id)
    
    try:
        course = Course.objects.get(id=course_id)
        payment_method = request.POST.get('payment_method')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('payment_page', course_id=course_id)
        
        if payment_method == 'esewa':
            # Generate transaction UUID
            transaction_uuid = str(uuid.uuid4())
            
            # Calculate amounts
            amount = str(course.price)
            tax_amount = "0"
            product_service_charge = "0"
            product_delivery_charge = "0"
            total_amount = str(course.price)  # Since tax and charges are 0
            
            # Store payment info in session
            payment_info = {
                'course_id': course.id,
                'amount': amount,
                'transaction_uuid': transaction_uuid,
                'timestamp': timezone.now().isoformat()
            }
            request.session['payment_info'] = payment_info
            
            # Prepare eSewa payment data
            payment_data = {
                'amt': amount,
                'txAmt': tax_amount,
                'psc': product_service_charge,
                'pdc': product_delivery_charge,
                'tAmt': total_amount,
                'pid': transaction_uuid,
                'scd': settings.ESEWA_MERCHANT_ID,
                'su': request.build_absolute_uri(reverse('esewa_success')),
                'fu': request.build_absolute_uri(reverse('esewa_failure'))
            }
            
            # Render eSewa payment template
            return render(request, 'payments/esewa_payment.html', {
                'course': course,
                'payment_data': payment_data,
                'esewa_url': settings.ESEWA_URL
            })
        else:
            messages.error(request, 'Invalid payment method selected.')
            return redirect('payment_page', course_id=course_id)
            
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_list')
    except Exception as e:
        messages.error(request, f'Payment failed: {str(e)}')
        return redirect('payment_page', course_id=course_id)

@login_required
def esewa_success(request):
    try:
        payment_info = request.session.get('payment_info')
        if not payment_info:
            messages.error(request, 'Invalid payment session.')
            return redirect('course_list')
        
        # Get the response data from eSewa
        refId = request.GET.get('refId')
        oid = request.GET.get('oid')
        amt = request.GET.get('amt')
        
        print(f"eSewa Response - refId: {refId}, oid: {oid}, amt: {amt}")  # Debug print
        
        if not all([refId, oid, amt]):
            messages.error(request, 'Invalid payment response from eSewa.')
            return redirect('course_list')
        
        # Verify payment with eSewa status check API
        status_check_url = f"{settings.ESEWA_STATUS_CHECK_URL}?product_code={settings.ESEWA_MERCHANT_ID}&total_amount={amt}&transaction_uuid={oid}"
        print(f"Status check URL: {status_check_url}")  # Debug print
        
        try:
            response = requests.get(status_check_url, timeout=10)
            print(f"Status check response status code: {response.status_code}")  # Debug print
            print(f"Status check response content: {response.text}")  # Debug print
            
            if response.status_code != 200:
                messages.error(request, f'Failed to verify payment status. Status code: {response.status_code}')
                return redirect('course_list')
            
            try:
                status_data = response.json()
                print(f"Status data: {status_data}")  # Debug print
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")  # Debug print
                messages.error(request, 'Invalid response from eSewa.')
                return redirect('course_list')
            
            if status_data.get('status') != 'COMPLETE':
                messages.error(request, f'Payment verification failed. Status: {status_data.get("status")}')
                return redirect('course_list')
            
            # Only now create the payment record
            course = Course.objects.get(id=payment_info['course_id'])
            
            # Check if payment already exists
            if Payment.objects.filter(transaction_id=refId).exists():
                messages.error(request, 'Payment already processed.')
                return redirect('course_detail', course_id=course.id)
            
            payment = Payment.objects.create(
                student=request.user,
                course=course,
                amount=amt,
                payment_method='esewa',
                status='completed',
                transaction_id=refId
            )
            
            # Create enrollment
            Enrollment.objects.create(
                student=request.user,
                course=course,
                progress=0,
                is_completed=False
            )
            
            # Clear payment session
            del request.session['payment_info']
            
            messages.success(request, 'Payment successful! You are now enrolled in the course.')
            return redirect('course_detail', course_id=course.id)
                
        except requests.RequestException as e:
            print(f"Request error: {str(e)}")  # Debug print
            messages.error(request, f'Error connecting to eSewa: {str(e)}')
            return redirect('course_list')
            
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_list')
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug print
        messages.error(request, f'Payment verification failed: {str(e)}')
        return redirect('course_list')

@login_required
def esewa_failure(request):
    try:
        # Clear payment session
        if 'payment_info' in request.session:
            del request.session['payment_info']
        
        messages.error(request, 'Payment failed. Please try again.')
        return redirect('course_list')
        
    except Exception as e:
        messages.error(request, f'Error processing payment failure: {str(e)}')
        return redirect('course_list')

@login_required
def manage_course_resources(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is the course instructor
    if not request.user == course.instructor:
        messages.error(request, "You don't have permission to manage this course's resources.")
        return redirect('course_detail', course_id=course_id)
    
    resources = course.resources.all()
    categories = course.resource_categories.all()
    
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = course
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, "Resource uploaded successfully!")
            return redirect('manage_course_resources', course_id=course_id)
    else:
        form = ResourceUploadForm()
    
    return render(request, 'courses/manage_resources.html', {
        'course': course,
        'resources': resources,
        'categories': categories,
        'form': form
    })

@login_required
def upload_resource(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is the course instructor
    if not request.user == course.instructor:
        messages.error(request, "You don't have permission to upload resources for this course.")
        return redirect('course_detail', course_id=course_id)
    
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = course
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, "Resource uploaded successfully!")
            return redirect('manage_course_resources', course_id=course_id)
    else:
        form = ResourceUploadForm()
    
    return render(request, 'courses/upload_resource.html', {
        'course': course,
        'form': form
    })

@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(CourseResource, id=resource_id)
    
    # Check if user is the course instructor
    if not request.user == resource.course.instructor:
        messages.error(request, "You don't have permission to delete this resource.")
        return redirect('course_detail', course_id=resource.course.id)
    
    if request.method == 'POST':
        resource.delete()
        messages.success(request, "Resource deleted successfully!")
        return redirect('manage_course_resources', course_id=resource.course.id)
    
    return render(request, 'courses/confirm_delete_resource.html', {
        'resource': resource
    })
