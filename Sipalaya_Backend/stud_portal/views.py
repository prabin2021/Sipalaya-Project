from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EnrolledCourse, CompletedLesson, Assignment, Attendance
from django.contrib import messages
from .models import StudentProfile,InstructorProfile,Profile
from .forms import UserRegistrationForm,StudentProfileForm,InstructorProfileForm
from django.urls import reverse
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

    profile_instance, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        role = request.POST.get('role')  # Grab role from form submission
        profile_instance.role = role
        profile_instance.save()

        if role == 'student':
            profile_form = StudentProfileForm(request.POST)
        else:
            profile_form = InstructorProfileForm(request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.has_completed_profile = True
            profile.save()

            if role == 'student':
                return redirect('stud_dashboard')
            else:
                return redirect('instructor_dashboard')
    else:
        profile_form = (
            StudentProfileForm() if profile_instance.role == 'student'
            else InstructorProfileForm()
        )

    return render(request, 'complete_profile.html', {
        'form': profile_form,
        'role': profile_instance.role,
        'role_choices': Profile.ROLE_CHOICES
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
    user = request.user
    try:
        instructor_profile = InstructorProfile.objects.get(user=user)
    except InstructorProfile.DoesNotExist:
        return redirect('complete_profile')  # or error message

    if not instructor_profile.has_completed_profile:
        return redirect('complete_profile')

    # Show instructor-specific data
    # For example, all courses they manage and their students
    courses = instructor_profile.courses.all()
    instructors = set()
    for course in courses:
        instructors.update(EnrolledCourse.objects.filter(course=course).values_list('instructors', flat=True))
    context = {
        'user': user,
        'instructor_profile': instructor_profile,
        'courses': courses,
        'instructors': instructors,
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