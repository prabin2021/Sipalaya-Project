from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Avg
from courses.models import Course, Module, Lesson, Assignment, Submission, Enrollment, LessonProgress
from .models import Resource, AssignmentFeedback, InstructorProfile
from .forms import CourseForm, LessonForm, ResourceForm, AssignmentForm, FeedbackForm, InstructorProfileForm
from .utils import is_instructor

@login_required
@user_passes_test(is_instructor)
def dashboard(request):
    """Instructor dashboard view showing overview of courses and activities."""
    # Get instructor's courses
    courses = Course.objects.filter(instructor=request.user)
    
    # Calculate statistics
    total_courses = courses.count()
    total_students = Enrollment.objects.filter(course__in=courses).values('student').distinct().count()
    pending_assignments = Submission.objects.filter(
        assignment__lesson__module__course__in=courses,
        status='pending'
    ).count()
    
    # Calculate course completion rate
    total_lessons = Lesson.objects.filter(module__course__in=courses).count()
    completed_lessons = LessonProgress.objects.filter(
        lesson__module__course__in=courses,
        completed=True
    ).count()
    completion_rate = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    # Get recent resources
    recent_resources = Resource.objects.filter(
        lesson__module__course__in=courses
    ).order_by('-created_at')[:6]
    
    # Get recent submissions
    recent_submissions = Submission.objects.filter(
        assignment__lesson__module__course__in=courses
    ).order_by('-submitted_at')[:5]
    
    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'pending_assignments': pending_assignments,
        'completion_rate': round(completion_rate, 1),
        'recent_resources': recent_resources,
        'recent_submissions': recent_submissions,
        'courses': courses,
    }
    
    return render(request, 'instructor/dashboard.html', context)

@login_required
@user_passes_test(is_instructor)
def course_list(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'instructor/course_list.html', {'courses': courses})

@login_required
@user_passes_test(is_instructor)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructor:course_list')
    else:
        form = CourseForm()
    
    return render(request, 'instructor/course_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(is_instructor)
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('instructor:course_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'instructor/course_form.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(is_instructor)
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('instructor:course_list')
    
    return render(request, 'instructor/course_confirm_delete.html', {'course': course})

@login_required
@user_passes_test(is_instructor)
def resource_upload(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Check if the lesson belongs to the instructor
    if lesson.module.course.instructor != request.user:
        messages.error(request, "You don't have permission to upload resources for this lesson.")
        return redirect('instructor:dashboard')
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.lesson = lesson
            resource.save()
            
            messages.success(request, f"Resource '{resource.title}' has been uploaded successfully.")
            return redirect('instructor:lesson_detail', lesson_id=lesson.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ResourceForm()
    
    context = {
        'form': form,
        'lesson': lesson,
        'course': lesson.module.course,
        'module': lesson.module,
    }
    return render(request, 'instructor/resource_form.html', context)

@login_required
@user_passes_test(is_instructor)
def assignment_list(request):
    assignments = Assignment.objects.filter(
        lesson__module__course__instructor=request.user
    ).select_related('lesson', 'lesson__module', 'lesson__module__course')
    
    return render(request, 'instructor/assignment_list.html', {'assignments': assignments})

@login_required
@user_passes_test(is_instructor)
def submission_list(request, assignment_id):
    assignment = get_object_or_404(
        Assignment, 
        id=assignment_id,
        lesson__module__course__instructor=request.user
    )
    submissions = Submission.objects.filter(assignment=assignment).select_related('student')
    
    return render(request, 'instructor/submission_list.html', {
        'assignment': assignment,
        'submissions': submissions
    })

@login_required
@user_passes_test(is_instructor)
def grade_submission(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        assignment__lesson__module__course__instructor=request.user
    )
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Try to get existing feedback or create new one
            feedback, created = AssignmentFeedback.objects.get_or_create(
                submission=submission,
                defaults={
                    'feedback': form.cleaned_data['feedback'],
                    'grade': form.cleaned_data['grade']
                }
            )
            
            # If feedback already existed, update it
            if not created:
                feedback.feedback = form.cleaned_data['feedback']
                feedback.grade = form.cleaned_data['grade']
                feedback.save()
            
            # Update submission status to graded
            submission.status = 'graded'
            submission.save()
            
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('instructor:assignment_submissions', assignment_id=submission.assignment.id)
    else:
        # If there's existing feedback, populate the form with it
        try:
            existing_feedback = submission.feedback
            form = FeedbackForm(initial={
                'feedback': existing_feedback.feedback,
                'grade': existing_feedback.grade
            })
        except AssignmentFeedback.DoesNotExist:
            form = FeedbackForm()
    
    return render(request, 'instructor/grade_submission.html', {
        'form': form,
        'submission': submission
    })

@login_required
@user_passes_test(is_instructor)
def student_progress(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, instructor=request.user)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    
    # Calculate progress for each student
    for enrollment in enrollments:
        total_lessons = Lesson.objects.filter(module__course=course).count()
        completed_lessons = LessonProgress.objects.filter(
            student=enrollment.student,
            lesson__module__course=course,
            completed=True
        ).count()
        enrollment.progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    return render(request, 'instructor/student_progress.html', {
        'course': course,
        'enrollments': enrollments
    })

@login_required
def profile_setup(request):
    profile, created = InstructorProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = InstructorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('instructor:dashboard')
    else:
        form = InstructorProfileForm(instance=profile)
    
    return render(request, 'instructor/profile_setup.html', {
        'profile': profile,
        'form': form
    })

@login_required
@user_passes_test(is_instructor)
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instructor=request.user)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('instructor:assignment_list')
    else:
        form = AssignmentForm(instructor=request.user)
    
    return render(request, 'instructor/assignment_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(is_instructor)
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        lesson__module__course__instructor=request.user
    )
    return render(request, 'instructor/assignment_detail.html', {'assignment': assignment})

@login_required
@user_passes_test(is_instructor)
def assignment_edit(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        lesson__module__course__instructor=request.user
    )
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment, instructor=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('instructor:assignment_list')
    else:
        form = AssignmentForm(instance=assignment, instructor=request.user)
    
    return render(request, 'instructor/assignment_form.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(is_instructor)
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    resources = Resource.objects.filter(lesson=lesson)
    
    context = {
        'lesson': lesson,
        'resources': resources,
    }
    return render(request, 'instructor/lesson_detail.html', context)

@login_required
@user_passes_test(is_instructor)
def module_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            module = Module.objects.create(
                course=course,
                title=title
            )
            messages.success(request, 'Module created successfully!')
            return redirect('instructor:course_edit', slug=course.slug)
        else:
            messages.error(request, 'Module title is required.')
            return redirect('instructor:course_edit', slug=course.slug)
    
    return render(request, 'instructor/module_form.html', {
        'course': course
    })

@login_required
@user_passes_test(is_instructor)
def module_edit(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            module.title = title
            module.save()
            messages.success(request, 'Module updated successfully!')
            return redirect('instructor:course_edit', slug=module.course.slug)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@user_passes_test(is_instructor)
def module_delete(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    
    if request.method == 'POST':
        course_slug = module.course.slug
        module.delete()
        messages.success(request, 'Module deleted successfully!')
        return redirect('instructor:course_edit', slug=course_slug)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@user_passes_test(is_instructor)
def lesson_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = form.cleaned_data['module']
            lesson.save()
            messages.success(request, 'Lesson created successfully!')
            return redirect('instructor:course_edit', slug=course.slug)
    else:
        form = LessonForm()
        # Filter modules to only show those belonging to this course
        form.fields['module'].queryset = Module.objects.filter(course=course)
    
    return render(request, 'instructor/lesson_form.html', {
        'form': form,
        'course': course
    })

@login_required
@user_passes_test(is_instructor)
def lesson_edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = form.cleaned_data['module']
            lesson.save()
            messages.success(request, 'Lesson updated successfully!')
            return redirect('instructor:course_edit', slug=lesson.module.course.slug)
    else:
        form = LessonForm(instance=lesson)
        # Filter modules to only show those belonging to this course
        form.fields['module'].queryset = Module.objects.filter(course=lesson.module.course)
    
    return render(request, 'instructor/lesson_form.html', {
        'form': form,
        'course': lesson.module.course,
        'action': 'Edit'
    })

@login_required
@user_passes_test(is_instructor)
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    
    if request.method == 'POST':
        course_slug = lesson.module.course.slug
        lesson.delete()
        messages.success(request, 'Lesson deleted successfully!')
        return redirect('instructor:course_edit', slug=course_slug)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def assignment_submissions(request, assignment_id):
    """View for listing all submissions for a specific assignment."""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Get all submissions for this assignment
    submissions = Submission.objects.filter(
        assignment=assignment
    ).select_related('student').order_by('-submitted_at')
    
    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'instructor/assignment_submissions.html', context)
