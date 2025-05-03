from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import EnrolledCourse, CompletedLesson, Assignment, Attendance
from django.contrib import messages
from .models import StudentProfile,InstructorProfile,Profile
from .forms import UserRegistrationForm,StudentProfileForm,InstructorProfileForm, CourseForm, AssignmentForm
from django.urls import reverse
from django.utils import timezone
from courses.models import Course, CourseResource
from django.contrib.auth import logout
from django.db.models import Avg
from django.contrib.auth.models import User
import json

def is_instructor(user):
    """Check if the user has an instructor profile."""
    return hasattr(user, 'instructorprofile') and user.instructorprofile.has_completed_profile

# 📌 **Student Dashboard: View enrolled courses, progress, and certificates**
# def student_dashboard(request):
#     enrolled_courses = EnrolledCourse.objects.filter(student=request.user)
    
#     # Get course details along with instructor and category
#     course_details = []
#     for enrolled_course in enrolled_courses:
#         course = enrolled_course.course
#         course_details.append({
#             'course': course,
#             'instructor': course.instructor,
#             'category': course.category,
#             'progress': enrolled_course.progress
#         })
    
#     return render(request, 'stud_dashboard.html', {'course_details': course_details})
@login_required
def role_based_dashboard(request):
    user = request.user

    if hasattr(user, 'studentprofile'):
        return redirect('student_dashboard')
    elif hasattr(user, 'instructorprofile'):
        return redirect('instructor_dashboard')
    elif user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('login')
@login_required
def complete_profile(request):
    user = request.user

    try:
        profile_instance = Profile.objects.get(user=user)
        if profile_instance.has_completed_profile:
            if profile_instance.role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('instructor_dashboard')
    except Profile.DoesNotExist:
        return redirect('login')  # User should have a profile assigned by admin

    if request.method == "POST":
        if profile_instance.role == 'student':
            try:
                profile = StudentProfile.objects.get(user=user)
                profile_form = StudentProfileForm(request.POST, instance=profile)
            except StudentProfile.DoesNotExist:
                profile_form = StudentProfileForm(request.POST)
        else:
            try:
                profile = InstructorProfile.objects.get(user=user)
                profile_form = InstructorProfileForm(request.POST, instance=profile)
            except InstructorProfile.DoesNotExist:
                profile_form = InstructorProfileForm(request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.has_completed_profile = True
            profile.save()

            if profile_instance.role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('instructor_dashboard')
    else:
        if profile_instance.role == 'student':
            try:
                profile = StudentProfile.objects.get(user=user)
                profile_form = StudentProfileForm(instance=profile)
            except StudentProfile.DoesNotExist:
                profile_form = StudentProfileForm()
        else:
            try:
                profile = InstructorProfile.objects.get(user=user)
                profile_form = InstructorProfileForm(instance=profile)
            except InstructorProfile.DoesNotExist:
                profile_form = InstructorProfileForm()

    return render(request, 'complete_profile.html', {
        'form': profile_form,
        'role': profile_instance.role
    })


@login_required
def student_dashboard(request):
    user = request.user
    try:
        student_profile = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        return redirect('complete_profile')  # or error message

    if not student_profile.has_completed_profile:
        return redirect('complete_profile')

    enrolled_courses = EnrolledCourse.objects.filter(student=user)
    attendance_records = Attendance.objects.filter(student=user)
    assignments = Assignment.objects.filter(student=user)

    context = {
        'user': user,
        'student_profile': student_profile,
        'enrolled_courses': enrolled_courses,
        'attendance_records': attendance_records,
        'assignments': assignments,
    }
    return render(request, 'stud_dashboard.html', context)


@login_required
def instructor_dashboard(request):
    # Check if user has instructor profile
    try:
        instructor_profile = InstructorProfile.objects.get(user=request.user)
        if not instructor_profile.has_completed_profile:
            return redirect('complete_profile')
    except InstructorProfile.DoesNotExist:
        return redirect('student_dashboard')
    
    # Get instructor's courses
    courses = Course.objects.filter(instructor=request.user)
    
    # Get all enrolled courses for these courses
    enrolled_courses = EnrolledCourse.objects.filter(course__in=courses)
    
    # Calculate statistics
    total_students = enrolled_courses.values('student').distinct().count()
    active_courses = courses.filter(is_active=True).count()
    
    # Get pending assignments
    pending_assignments = Assignment.objects.filter(
        course__in=enrolled_courses,
        status='pending'
    ).count()
    
    # Get recent activities
    recent_activities = []
    for course in courses:
        # Add recent enrollments
        recent_enrollments = EnrolledCourse.objects.filter(
            course=course,
            enrollment_date__gte=timezone.now() - timezone.timedelta(days=7)
        )
        for enrollment in recent_enrollments:
            recent_activities.append({
                'title': f'New Enrollment: {enrollment.student.username}',
                'description': f'Enrolled in {course.title}',
                'timestamp': enrollment.enrollment_date
            })
        
        # Add recent assignments
        recent_submissions = Assignment.objects.filter(
            course__course=course,
            submitted_at__gte=timezone.now() - timezone.timedelta(days=7)
        )
        for submission in recent_submissions:
            recent_activities.append({
                'title': f'New Assignment Submission: {submission.student.username}',
                'description': f'Submitted {submission.title or "Untitled Assignment"} for {course.title}',
                'timestamp': submission.submitted_at
            })
    
    # Sort activities by timestamp
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activities = recent_activities[:10]
    
    # Get student performance data
    student_performance = []
    for enrollment in enrolled_courses:
        assignments = Assignment.objects.filter(
            student=enrollment.student,
            course=enrollment
        )
        completed_count = assignments.filter(status='completed').count()
        total_count = assignments.count()
        average_grade = assignments.aggregate(Avg('marks_obtained'))['marks_obtained__avg']
        
        student_performance.append({
            'student': enrollment.student,
            'course': enrollment.course,
            'progress': enrollment.progress,
            'assignments_completed': completed_count,
            'total_assignments': total_count,
            'average_grade': average_grade or 0.0
        })
    
    context = {
        'courses': courses,
        'total_students': total_students,
        'active_courses': active_courses,
        'pending_assignments': pending_assignments,
        'recent_activities': recent_activities,
        'student_performance': student_performance
    }
    
    return render(request, 'instructor_dashboard.html', context)
# 📌 **Mark Lesson as Completed**
@login_required
def mark_lesson_completed(request, lesson_id):
    # Removed the Lesson-related code
    student = request.user

    # Find the lesson that the student completed (without Lesson model)
    if not CompletedLesson.objects.filter(student=student, lesson_id=lesson_id).exists():
        CompletedLesson.objects.create(student=student, lesson_id=lesson_id)
        update_progress(student)

    messages.success(request, "You have completed the lesson.")
    return redirect('course_detail', course_id=lesson_id)  # Assuming you have a 'course_detail' view


# 📌 **Update Progress Calculation**
def update_progress(student):
    # Calculate progress based on enrolled courses and completed lessons
    enrolled_courses = EnrolledCourse.objects.filter(student=student)
    for enrolled_course in enrolled_courses:
        total_lessons = enrolled_course.course.lesson_set.count()  # Assumes course has lessons linked to it
        completed_lessons = CompletedLesson.objects.filter(student=student, lesson__course=enrolled_course.course).count()

        progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0

        enrolled_course.progress = progress
        enrolled_course.save()


# 📌 **Assignment Submission**
@login_required
def submit_assignment(request, course_id):
    course = get_object_or_404(EnrolledCourse, id=course_id)
    
    if request.method == 'POST':
        uploaded_file = request.FILES.get('assignment_file')
        
        if uploaded_file:
            Assignment.objects.create(student=request.user, course=course, file=uploaded_file)
            messages.success(request, "Assignment submitted successfully!")
        else:
            messages.error(request, "Please upload a valid file.")

        return redirect('student_dashboard')

    return render(request, 'student_portal/submit_assignment.html', {'course': course})


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

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def manage_assignments(request, course_id):
    # Check if user has instructor profile
    if not hasattr(request.user, 'instructorprofile'):
        return redirect('student_dashboard')
    
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    enrolled_courses = EnrolledCourse.objects.filter(course=course)
    assignments = Assignment.objects.filter(course__in=enrolled_courses)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            # Get the first enrolled course for this course
            enrolled_course = enrolled_courses.first()
            if enrolled_course:
                assignment.course = enrolled_course
                assignment.student = request.user
                assignment.save()
                messages.success(request, 'Assignment created successfully!')
                return redirect('manage_assignments', course_id=course_id)
            else:
                messages.error(request, 'No students enrolled in this course yet.')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AssignmentForm()
    
    context = {
        'course': course,
        'assignments': assignments,
        'form': form
    }
    return render(request, 'manage_assignments.html', context)

@login_required
def grade_assignment(request, assignment_id):
    if not request.user.is_instructor:
        return redirect('student_dashboard')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if assignment.course.instructor != request.user:
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = GradeAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.status = 'graded'
            assignment.save()
            messages.success(request, 'Assignment graded successfully!')
            return redirect('manage_assignments', course_id=assignment.course.id)
    else:
        form = GradeAssignmentForm(instance=assignment)
    
    context = {
        'assignment': assignment,
        'form': form
    }
    return render(request, 'grade_assignment.html', context)

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def create_course(request):
    if not hasattr(request.user, 'instructorprofile'):
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {
        'form': form,
        'title': 'Create Course'
    })

@login_required
def edit_course(request, course_id):
    if not hasattr(request.user, 'instructorprofile'):
        return redirect('student_dashboard')
    
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form.html', {
        'form': form,
        'title': 'Edit Course',
        'course': course
    })

@login_required
def delete_course(request, course_id):
    if not hasattr(request.user, 'instructorprofile'):
        return redirect('student_dashboard')
    
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('instructor_dashboard')
    
    return render(request, 'courses/confirm_delete.html', {
        'course': course
    })

@login_required
def student_detail(request, student_id):
    if not hasattr(request.user, 'instructorprofile'):
        return redirect('student_dashboard')
    
    student = get_object_or_404(User, id=student_id)
    courses = Course.objects.filter(instructor=request.user)
    enrollments = EnrolledCourse.objects.filter(student=student, course__in=courses)
    
    # Get student performance data
    performance_data = []
    for enrollment in enrollments:
        assignments = Assignment.objects.filter(
            student=student,
            course=enrollment.course
        )
        
        performance_data.append({
            'course': enrollment.course,
            'progress': enrollment.progress,
            'assignments_completed': assignments.filter(status='completed').count(),
            'total_assignments': assignments.count(),
            'average_grade': assignments.aggregate(Avg('grade'))['grade__avg'],
            'last_activity': assignments.order_by('-submitted_at').first()
        })
    
    return render(request, 'student_detail.html', {
        'student': student,
        'performance_data': performance_data
    })

@login_required
@user_passes_test(is_instructor)
def bulk_grade_assignments(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = BulkGradeForm(request.POST)
        if form.is_valid():
            grades_data = json.loads(form.cleaned_data['grades'])
            feedback = form.cleaned_data['feedback']
            
            for submission_id, grade in grades_data.items():
                submission = get_object_or_404(AssignmentSubmission, id=submission_id)
                submission.grade = grade
                submission.feedback = feedback
                submission.graded_by = request.user
                submission.graded_at = timezone.now()
                submission.save()
            
            messages.success(request, 'Grades updated successfully')
            return redirect('manage_assignments', course_id=course_id)
    else:
        form = BulkGradeForm()
    
    submissions = AssignmentSubmission.objects.filter(
        assignment__course=course,
        grade__isnull=True
    ).select_related('student', 'assignment')
    
    return render(request, 'bulk_grade.html', {
        'course': course,
        'form': form,
        'submissions': submissions
    })

@login_required
@user_passes_test(is_instructor)
def create_grading_rubric(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = GradingRubricForm(request.POST)
        if form.is_valid():
            criteria = form.cleaned_data['criteria'].split('\n')
            max_points = form.cleaned_data['max_points']
            
            # Create rubric entries
            for criterion in criteria:
                if criterion.strip():
                    Rubric.objects.create(
                        assignment=assignment,
                        criterion=criterion.strip(),
                        max_points=max_points
                    )
            
            messages.success(request, 'Grading rubric created successfully')
            return redirect('manage_assignments', course_id=assignment.course.id)
    else:
        form = GradingRubricForm()
    
    return render(request, 'create_rubric.html', {
        'assignment': assignment,
        'form': form
    })

@login_required
@user_passes_test(is_instructor)
def view_rubric(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    rubric = Rubric.objects.filter(assignment=assignment)
    return render(request, 'view_rubric.html', {
        'assignment': assignment,
        'rubric': rubric
    })