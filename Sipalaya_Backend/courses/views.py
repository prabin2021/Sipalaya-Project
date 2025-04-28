from django.shortcuts import render, get_object_or_404
from instructor_portal.models import Course, Lesson, CourseMaterial, Resource
from courses.models import Category

def course_list(request):
    courses = Course.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses, 'categories': categories})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    lessons = course.lessons.all().order_by('order')
    materials = course.materials.all()
    resources = course.resources.all()
    announcements = course.announcements.all().order_by('-created_at')[:5]  # Latest 5 announcements
    
    context = {
        'course': course,
        'lessons': lessons,
        'materials': materials,
        'resources': resources,
        'announcements': announcements,
    }
    return render(request, 'courses/course_detail.html', context)

def course_syllabus(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    lessons = course.lessons.all().order_by('order')
    materials = course.materials.all()
    resources = course.resources.all()
    
    context = {
        'course': course,
        'lessons': lessons,
        'materials': materials,
        'resources': resources,
    }
    return render(request, 'courses/course_syllabus.html', context)

def courses_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category, is_active=True)
    return render(request, 'courses/course_list.html', {'courses': courses, 'category': category})
