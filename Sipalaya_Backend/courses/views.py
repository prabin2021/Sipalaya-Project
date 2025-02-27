from django.shortcuts import render, get_object_or_404
from .models import Course, Category

def course_list(request):
    courses = Course.objects.all()
    categories = Category.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses, 'categories': categories})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    syllabus_items = course.syllabus.split("\n")
    prerequisites = course.prerequisites.split("\n")
    return render(request, 'courses/course_detail.html', {'course': course, 'syllabus_items': syllabus_items, 'prerequisites': prerequisites,})

def courses_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/course_list.html', {'courses': courses, 'category': category})
