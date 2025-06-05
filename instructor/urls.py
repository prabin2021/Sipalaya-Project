from django.urls import path
from . import views

app_name = 'instructor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<slug:slug>/edit/', views.course_edit, name='course_edit'),
    path('courses/<slug:slug>/delete/', views.course_delete, name='course_delete'),
    path('courses/<slug:course_slug>/progress/', views.student_progress, name='student_progress'),
    path('modules/<int:course_id>/create/', views.module_create, name='module_create'),
    path('modules/<int:module_id>/edit/', views.module_edit, name='module_edit'),
    path('modules/<int:module_id>/delete/', views.module_delete, name='module_delete'),
    path('lessons/<int:course_id>/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),
    path('lessons/<int:lesson_id>/resources/upload/', views.resource_upload, name='resource_upload'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:assignment_id>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignments/<int:assignment_id>/submissions/', views.assignment_submissions, name='assignment_submissions'),
    path('submissions/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
] 