from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DemoClass, DemoClassSchedule, DemoClassBooking, DemoClassFeedback
from .forms import DemoClassForm, DemoClassScheduleForm, DemoClassBookingForm, DemoClassFeedbackForm
from django.core.paginator import Paginator
from django.db.models import Q
from .emails import send_booking_confirmation, send_booking_cancellation, send_reminder

def demo_class_list(request):
    """List all available demo classes"""
    demo_classes = DemoClass.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        demo_classes = demo_classes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(course__title__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(demo_classes, 9)
    page = request.GET.get('page')
    demo_classes = paginator.get_page(page)
    
    context = {
        'demo_classes': demo_classes,
        'search_query': search_query,
        'now': timezone.now(),
    }
    return render(request, 'demo_classes/list.html', context)

@login_required
def demo_class_detail(request, demo_class_id):
    """View details of a specific demo class"""
    demo_class = get_object_or_404(DemoClass, id=demo_class_id)
    available_schedules = DemoClassSchedule.objects.filter(
        demo_class=demo_class,
        is_booked=False,
        start_time__gt=timezone.now()
    ).order_by('start_time')
    
    context = {
        'demo_class': demo_class,
        'available_schedules': available_schedules,
        'now': timezone.now(),
    }
    return render(request, 'demo_classes/detail.html', context)

@login_required
def book_demo_class(request, schedule_id):
    """Book a demo class"""
    schedule = get_object_or_404(DemoClassSchedule, id=schedule_id)
    
    if schedule.is_booked:
        messages.error(request, "This time slot is already booked.")
        return redirect('demo_classes:detail', demo_class_id=schedule.demo_class.id)
    
    if request.method == 'POST':
        form = DemoClassBookingForm(request.POST)
        if form.is_valid():
            # Create booking directly instead of using form.save()
            booking = DemoClassBooking.objects.create(
                user=request.user,
                schedule=schedule,
                status='confirmed',
                notes=form.cleaned_data.get('notes', '')
            )
            
            # Update schedule status
            schedule.is_booked = True
            schedule.save()
            
            # Send confirmation email
            send_booking_confirmation(booking)
            
            messages.success(request, "Your demo class booking has been confirmed!")
            return redirect('demo_classes:my_bookings')
    else:
        form = DemoClassBookingForm()
    
    context = {
        'form': form,
        'schedule': schedule,
    }
    return render(request, 'demo_classes/book.html', context)

@login_required
def my_bookings(request):
    """View user's demo class bookings"""
    bookings = DemoClassBooking.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'now': timezone.now(),
    }
    return render(request, 'demo_classes/my_bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    """Cancel a demo class booking"""
    booking = get_object_or_404(DemoClassBooking, id=booking_id, user=request.user)
    
    if booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
        
        # Make the schedule available again
        schedule = booking.schedule
        schedule.is_booked = False
        schedule.save()
        
        # Send cancellation email
        send_booking_cancellation(booking)
        
        messages.success(request, "Your booking has been cancelled.")
    
    return redirect('demo_classes:my_bookings')

@login_required
def submit_feedback(request, booking_id):
    """Submit feedback for a completed demo class"""
    booking = get_object_or_404(DemoClassBooking, id=booking_id, user=request.user)
    
    # Check if feedback already exists
    if hasattr(booking, 'feedback'):
        messages.error(request, "You have already submitted feedback for this demo class.")
        return redirect('demo_classes:my_bookings')
    
    if request.method == 'POST':
        form = DemoClassFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.booking = booking
            feedback.save()
            
            messages.success(request, 'Thank you for your feedback!')
            return redirect('demo_classes:my_bookings')
    else:
        form = DemoClassFeedbackForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'demo_classes/feedback.html', context)

# Admin views
@login_required
def create_demo_class(request):
    """Create a new demo class (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create demo classes.")
        return redirect('demo_classes:list')
    
    if request.method == 'POST':
        form = DemoClassForm(request.POST)
        if form.is_valid():
            demo_class = form.save()
            messages.success(request, "Demo class created successfully!")
            return redirect('demo_classes:detail', demo_class_id=demo_class.id)
    else:
        form = DemoClassForm()
    
    context = {
        'form': form,
    }
    return render(request, 'demo_classes/admin/create_demo_class.html', context)

@login_required
def create_schedule(request, demo_class_id):
    """Create a schedule for a demo class (admin only)"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create schedules.")
        return redirect('demo_classes:list')
    
    demo_class = get_object_or_404(DemoClass, id=demo_class_id)
    
    if request.method == 'POST':
        form = DemoClassScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.demo_class = demo_class
            schedule.save()
            messages.success(request, "Schedule created successfully!")
            return redirect('demo_classes:detail', demo_class_id=demo_class.id)
    else:
        form = DemoClassScheduleForm(initial={'demo_class': demo_class})
    
    context = {
        'form': form,
        'demo_class': demo_class,
    }
    return render(request, 'demo_classes/admin/create_schedule.html', context) 