from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Enrollment
from .models import Testimonial, Review

# Create your views here.

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
        return redirect('feedback:testimonials')
    
    return render(request, 'feedback/testimonial_form.html')

@login_required
def add_review(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    
    # Check if user is enrolled in the course
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled in the course to leave a review.')
        return redirect('courses:course_detail', slug=course_slug)
    
    # Check if user has already reviewed
    existing_review = Review.objects.filter(student=request.user, course=course).first()
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        
        if existing_review:
            existing_review.rating = rating
            existing_review.content = content
            existing_review.save()
            messages.success(request, 'Your review has been updated.')
        else:
            Review.objects.create(
                student=request.user,
                course=course,
                rating=rating,
                content=content
            )
            messages.success(request, 'Your review has been submitted for review.')
        
        return redirect('courses:course_detail', slug=course_slug)
    
    return render(request, 'feedback/review_form.html', {
        'course': course,
        'existing_review': existing_review
    })

def testimonials(request):
    testimonials = Testimonial.objects.filter(is_approved=True)
    return render(request, 'feedback/testimonials.html', {
        'testimonials': testimonials
    })
