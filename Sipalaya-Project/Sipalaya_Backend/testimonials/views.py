from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Testimonial, Review
from courses.models import Course
from django.http import JsonResponse

def testimonial_list(request):
    testimonials = Testimonial.objects.filter(is_approved=True)
    return render(request, 'testimonials/testimonial_list.html', {
        'testimonials': testimonials
    })

@login_required
def add_testimonial(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        job_title = request.POST.get('job_title')
        company = request.POST.get('company')
        photo = request.FILES.get('photo')
        
        testimonial = Testimonial.objects.create(
            student=request.user,
            course=course,
            content=content,
            rating=rating,
            job_title=job_title,
            company=company,
            photo=photo
        )
        
        messages.success(request, 'Your testimonial has been submitted and is pending approval.')
        return redirect('course_detail', course_id=course_id)
    
    return render(request, 'testimonials/add_testimonial.html', {
        'course': course
    })

@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        
        review, created = Review.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={
                'content': content,
                'rating': rating
            }
        )
        
        if not created:
            review.content = content
            review.rating = rating
            review.save()
        
        messages.success(request, 'Your review has been submitted and is pending approval.')
        return redirect('course_detail', course_id=course_id)
    
    return render(request, 'testimonials/add_review.html', {
        'course': course
    })

def get_course_reviews(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = Review.objects.filter(course=course, is_approved=True)
    
    reviews_data = [{
        'student_name': review.student.get_full_name(),
        'rating': review.rating,
        'content': review.content,
        'created_at': review.created_at.strftime('%B %d, %Y')
    } for review in reviews]
    
    return JsonResponse({'reviews': reviews_data})
