from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EnrolledCourse, CompletedLesson, Assignment, Attendance
from django.contrib import messages

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

def student_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        enrolled_courses = EnrolledCourse.objects.filter(student=user)
        attendance_records = Attendance.objects.filter(student=user)
        assignments = Assignment.objects.filter(student=user)
        context = {
            'user': user,
            'enrolled_courses': enrolled_courses,
            'attendance_records': attendance_records,
            'assignments': assignments,
        }
        return render(request, 'stud_dashboard.html', context)
    else:
        return redirect('login')

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
