from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Announcement, Resource, Assignment, CourseMaterial
from stud_portal.models import EnrolledCourse, CompletedLesson, Assignment as StudentAssignment
from .forms import CourseForm, LessonForm, ResourceForm, AssignmentForm, AssignmentGradingForm, AnnouncementForm, CourseMaterialForm
from django.contrib import messages
from django.db.models import Avg
from django.utils import timezone

@login_required
def instructor_dashboard(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    instructor_courses = Course.objects.filter(instructor=request.user)
    enrolled_students = EnrolledCourse.objects.filter(course__instructor=request.user)
    assignments = StudentAssignment.objects.filter(course__instructor=request.user)
    
    # Calculate average progress
    average_progress = enrolled_students.aggregate(Avg('progress'))['progress__avg'] or 0
    
    # Get recent activities
    recent_activities = []
    
    # Recent course enrollments
    recent_enrollments = enrolled_students.order_by('-enrolled_date')[:5]
    for enrollment in recent_enrollments:
        recent_activities.append({
            'icon': 'fas fa-user-plus',
            'description': f'New student enrolled in {enrollment.course.title}',
            'timestamp': enrollment.enrolled_date
        })
    
    # Recent assignment submissions
    recent_submissions = assignments.order_by('-submitted_date')[:5]
    for submission in recent_submissions:
        recent_activities.append({
            'icon': 'fas fa-file-upload',
            'description': f'New assignment submitted for {submission.course.title}',
            'timestamp': submission.submitted_date
        })
    
    # Recent announcements
    recent_announcements = Announcement.objects.filter(
        course__instructor=request.user
    ).order_by('-created_at')[:5]
    for announcement in recent_announcements:
        recent_activities.append({
            'icon': 'fas fa-bullhorn',
            'description': f'New announcement: {announcement.title}',
            'timestamp': announcement.created_at
        })
    
    # Sort activities by timestamp
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    context = {
        'total_courses': instructor_courses.count(),
        'total_students': enrolled_students.count(),
        'total_assignments': assignments.count(),
        'average_progress': round(average_progress, 1),
        'recent_activities': recent_activities[:5],
    }
    
    return render(request, 'instructor/dashboard.html', context)

@login_required
def manage_courses(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'instructor/manage_courses.html', {'courses': courses})

@login_required
def add_course(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('manage_courses')
    else:
        form = CourseForm()
    return render(request, 'instructor/add_course.html', {'form': form, 'courses': Course.objects.filter(instructor=request.user)})

@login_required
def edit_course(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'instructor/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('manage_courses')
    return render(request, 'instructor/delete_course.html', {'course': course})

@login_required
def manage_lessons(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'instructor/manage_lessons.html', {'course': course, 'lessons': lessons})

@login_required
def add_lesson(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson added successfully!")
            return redirect('manage_lessons', course_id=course.id)
    else:
        form = LessonForm()
    return render(request, 'instructor/add_lesson.html', {'form': form, 'course': course})

@login_required
def edit_lesson(request, lesson_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    lesson = get_object_or_404(Lesson, id=lesson_id, course__instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully!")
            return redirect('manage_lessons', course_id=lesson.course.id)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'instructor/edit_lesson.html', {'form': form, 'lesson': lesson})

@login_required
def delete_lesson(request, lesson_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    lesson = get_object_or_404(Lesson, id=lesson_id, course__instructor=request.user)
    if request.method == 'POST':
        course_id = lesson.course.id
        lesson.delete()
        messages.success(request, "Lesson deleted successfully!")
        return redirect('manage_lessons', course_id=course_id)
    return render(request, 'instructor/delete_lesson.html', {'lesson': lesson})

@login_required
def manage_announcements(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    announcements = Announcement.objects.filter(course=course)
    return render(request, 'instructor/manage_announcements.html', {'course': course, 'announcements': announcements})

@login_required
def add_announcement(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.course = course
            announcement.save()
            messages.success(request, "Announcement added successfully!")
            return redirect('manage_announcements', course_id=course.id)
    else:
        form = AnnouncementForm()
    return render(request, 'instructor/add_announcement.html', {'form': form, 'course': course})

@login_required
def manage_resources(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    resources = Resource.objects.filter(course=course)
    return render(request, 'instructor/manage_resources.html', {'course': course, 'resources': resources})

@login_required
def add_resource(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = course
            resource.save()
            messages.success(request, "Resource added successfully!")
            return redirect('manage_resources', course_id=course.id)
    else:
        form = ResourceForm()
    return render(request, 'instructor/add_resource.html', {'form': form, 'course': course})

@login_required
def manage_assignments(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    assignments = Assignment.objects.filter(course=course)
    return render(request, 'instructor/manage_assignments.html', {'course': course, 'assignments': assignments})

@login_required
def add_assignment(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, "Assignment added successfully!")
            return redirect('manage_assignments', course_id=course.id)
    else:
        form = AssignmentForm()
    return render(request, 'instructor/add_assignment.html', {'form': form, 'course': course})

@login_required
def grade_assignment(request, assignment_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    assignment = get_object_or_404(StudentAssignment, id=assignment_id, course__instructor=request.user)
    if request.method == 'POST':
        form = AssignmentGradingForm(request.POST)
        if form.is_valid():
            assignment.grade = form.cleaned_data['grade']
            assignment.feedback = form.cleaned_data['feedback']
            assignment.graded = True
            assignment.save()
            messages.success(request, "Assignment graded successfully!")
            return redirect('manage_assignments', course_id=assignment.course.id)
    else:
        form = AssignmentGradingForm(initial={
            'grade': assignment.grade,
            'feedback': assignment.feedback
        })
    return render(request, 'instructor/grade_assignment.html', {'form': form, 'assignment': assignment})

@login_required
def student_progress(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    enrolled_students = EnrolledCourse.objects.filter(course=course)
    return render(request, 'instructor/student_progress.html', {'course': course, 'enrolled_students': enrolled_students})

@login_required
def view_syllabus(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    lessons = Lesson.objects.filter(course=course).order_by('order')
    return render(request, 'instructor/view_syllabus.html', {
        'course': course,
        'lessons': lessons
    })

@login_required
def manage_materials(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    materials = CourseMaterial.objects.filter(course=course)
    return render(request, 'instructor/manage_materials.html', {
        'course': course,
        'materials': materials
    })

@login_required
def add_material(request, course_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, "Material added successfully!")
            return redirect('manage_materials', course_id=course.id)
    else:
        form = CourseMaterialForm()
    return render(request, 'instructor/add_material.html', {
        'form': form,
        'course': course
    })
