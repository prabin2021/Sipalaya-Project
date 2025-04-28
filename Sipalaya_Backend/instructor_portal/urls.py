from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('courses/<int:course_id>/syllabus/', views.view_syllabus, name='view_syllabus'),
    path('courses/<int:course_id>/lessons/', views.manage_lessons, name='manage_lessons'),
    path('courses/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('courses/<int:course_id>/assignments/', views.manage_assignments, name='manage_assignments'),
    path('courses/<int:course_id>/assignments/add/', views.add_assignment, name='add_assignment'),
    path('assignments/<int:assignment_id>/grade/', views.grade_assignment, name='grade_assignment'),
    path('courses/<int:course_id>/resources/', views.manage_resources, name='manage_resources'),
    path('courses/<int:course_id>/resources/add/', views.add_resource, name='add_resource'),
    path('courses/<int:course_id>/materials/', views.manage_materials, name='manage_materials'),
    path('courses/<int:course_id>/materials/add/', views.add_material, name='add_material'),
    path('courses/<int:course_id>/progress/', views.student_progress, name='student_progress'),
    path('courses/<int:course_id>/announcements/', views.manage_announcements, name='manage_announcements'),
    path('courses/<int:course_id>/announcements/add/', views.add_announcement, name='add_announcement'),
]