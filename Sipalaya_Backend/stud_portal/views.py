from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EnrolledCourse, CompletedLesson, Assignment, Attendance
from instructor_portal.models import Course, Lesson  # Assuming courses and lessons are managed by instructors
from django.contrib import messages
from .forms import AssignmentSubmissionForm

# 📌 **Student Dashboard: View enrolled courses, progress, and certificates**
@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('instructor_dashboard')
        
    enrolled_courses = EnrolledCourse.objects.filter(student=request.user)
    completed_lessons = CompletedLesson.objects.filter(student=request.user)
    pending_assignments = Assignment.objects.filter(
        student=request.user,
        graded=False
    )
    
    context = {
        'enrolled_courses': enrolled_courses,
        'completed_lessons_count': completed_lessons.count(),
        'pending_assignments_count': pending_assignments.count(),
    }
    
    return render(request, 'student/dashboard.html', context)


@login_required
def mark_lesson_completed(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = request.user
    
    if not CompletedLesson.objects.filter(student=student, lesson=lesson).exists():
        CompletedLesson.objects.create(student=student, lesson=lesson)
        update_progress(student, lesson.course)

    messages.success(request, f"You have completed: {lesson.title}")
    return redirect('course_detail', course_id=lesson.course.id)


def update_progress(student, course):
    total_lessons = Lesson.objects.filter(course=course).count()
    completed_lessons = CompletedLesson.objects.filter(student=student, lesson__course=course).count()

    progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0

    enrolled_course = EnrolledCourse.objects.get(student=student, course=course)
    enrolled_course.progress = progress
    enrolled_course.save()


# 📌 **Assignment Submission**
@login_required
def submit_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.course = course
            assignment.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect('student_dashboard')
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'student_portal/submit_assignment.html', {'form': form, 'course': course})


# 📌 **View Submitted Assignments and Feedback**
@login_required
def view_assignments(request):
    assignments = Assignment.objects.filter(student=request.user)
    return render(request, 'student_portal/view_assignments.html', {'assignments': assignments})


# 📌 **View Attendance Records**
@login_required
def view_attendance(request):
    attendance_records = Attendance.objects.filter(student=request.user)
    return render(request, 'student_portal/attendance.html', {'attendance_records': attendance_records})


@login_required
def enroll_course(request, course_id):
    if request.user.is_staff:
        return redirect('instructor_dashboard')
        
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    if EnrolledCourse.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course!")
        return redirect('course_detail', course_id=course.id)
    
    # Create enrollment
    EnrolledCourse.objects.create(student=request.user, course=course)
    messages.success(request, f"Successfully enrolled in {course.title}!")
    return redirect('course_detail', course_id=course.id)
