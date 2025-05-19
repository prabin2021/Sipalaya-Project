from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from courses.models import (
    Course, Enrollment, Assignment, 
    DemoClassBooking, Lesson, Module, LessonProgress, Review, Submission
)
from courses.forms import ReviewForm
from instructor.models import Resource
from django.http import FileResponse
from django.db.models import Count, Avg

# Create your views here.

@login_required
def dashboard(request):
    # Get enrolled courses
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    # Calculate progress for each course
    for enrollment in enrollments:
        total_lessons = Lesson.objects.filter(module__course=enrollment.course).count()
        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__module__course=enrollment.course,
            completed=True
        ).count()
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
    
    # Get graded assignments with feedback
    graded_assignments = Submission.objects.filter(
        student=request.user,
        status='graded'
    ).select_related(
        'assignment',
        'assignment__lesson',
        'assignment__lesson__module',
        'assignment__lesson__module__course',
        'feedback'
    ).order_by('-submitted_at')[:5]
    
    # Get attendance records
    attendance_records = DemoClassBooking.objects.filter(
        student=request.user,
        demo_class__date__gte=timezone.now().date() - timezone.timedelta(days=30)
    ).select_related('demo_class', 'demo_class__course').order_by('-demo_class__date')
    
    context = {
        'enrollments': enrollments,
        'recent_assignments': recent_assignments,
        'upcoming_assignments': upcoming_assignments,
        'graded_assignments': graded_assignments,
        'attendance_records': attendance_records,
        'now': timezone.now(),
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def course_progress(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    modules = course.modules.all()
    
    # Calculate progress for each module
    module_progress = {}
    total_completed = 0
    total_lessons = 0
    
    for module in modules:
        module_lessons = module.lessons.all()
        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__in=module_lessons,
            completed=True
        ).count()
        
        total_lessons_in_module = module_lessons.count()
        total_lessons += total_lessons_in_module
        total_completed += completed_lessons
        
        module_progress[module.id] = {
            'completed': completed_lessons,
            'total': total_lessons_in_module,
            'percentage': (completed_lessons / total_lessons_in_module * 100) if total_lessons_in_module > 0 else 0
        }
    
    # Calculate overall progress
    progress_percentage = (total_completed / total_lessons * 100) if total_lessons > 0 else 0
    
    return render(request, 'student/course_progress.html', {
        'course': course,
        'enrollment': enrollment,
        'modules': modules,
        'module_progress': module_progress,
        'progress_percentage': progress_percentage
    })

@login_required
def enrolled_courses(request):
    """View for displaying all enrolled courses."""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    # Calculate progress for each course
    for enrollment in enrollments:
        total_lessons = Lesson.objects.filter(module__course=enrollment.course).count()
        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__module__course=enrollment.course,
            completed=True
        ).count()
        enrollment.progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    return render(request, 'student/enrolled_courses.html', {
        'enrollments': enrollments
    })

@login_required
def course_content(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    modules = course.modules.all()
    
    # Get all lesson progress for this course and user
    lesson_progress = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        completed=True
    ).values_list('lesson_id', flat=True)
    
    # Create a dictionary of lesson_id: is_completed
    progress_dict = {lesson_id: True for lesson_id in lesson_progress}
    
    # Get user's review if it exists
    user_review = Review.objects.filter(student=request.user, course=course).first()
    
    # Calculate average rating
    avg_rating = course.reviews.aggregate(avg=Avg('rating'))['avg']
    
    return render(request, 'student/course_content.html', {
        'course': course,
        'enrollment': enrollment,
        'modules': modules,
        'progress_dict': progress_dict,
        'user_review': user_review,
        'avg_rating': avg_rating
    })

@login_required
def lesson_detail(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    return render(request, 'student/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment
    })

@login_required
def mark_lesson_complete(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    # Mark lesson as complete
    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson,
        defaults={'completed': True}
    )
    
    if not created:
        progress.completed = True
        progress.save()
    
    messages.success(request, 'Lesson marked as complete')
    return redirect('student:lesson_detail', slug=slug, lesson_id=lesson_id)

@login_required
def add_review(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        review, created = Review.objects.get_or_create(
            course=course,
            student=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            review.rating = rating
            review.comment = comment
            review.save()
        
        messages.success(request, 'Review submitted successfully')
        return redirect('student:course_content', slug=slug)
    
    return render(request, 'student/add_review.html', {
        'course': course
    })

@login_required
def edit_review(request, slug):
    course = get_object_or_404(Course, slug=slug)
    review = get_object_or_404(Review, course=course, student=request.user)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))  # Convert rating to integer
        comment = request.POST.get('comment')
        
        review.rating = rating
        review.comment = comment
        review.save()
        
        messages.success(request, 'Review updated successfully')
        return redirect('student:course_content', slug=slug)
    
    return render(request, 'student/edit_review.html', {
        'course': course,
        'review': review
    })