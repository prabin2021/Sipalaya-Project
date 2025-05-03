from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import register_view
from courses.views import manage_course_resources, delete_resource

urlpatterns = [
    path('register/', register_view, name='register'),
    path('dashboard/', views.role_based_dashboard, name='dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_completed, name='mark_lesson_completed'),
    path('assignments/submit/<int:course_id>/', views.submit_assignment, name='submit_assignment'),
    path('assignments/view/', views.view_assignments, name='view_assignments'),
    path('assignments/manage/<int:course_id>/', views.manage_assignments, name='manage_assignments'),
    path('assignments/grade/<int:assignment_id>/', views.grade_assignment, name='grade_assignment'),
    path('attendance/', views.view_attendance, name='view_attendance'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('resources/manage/<int:course_id>/', manage_course_resources, name='manage_course_resources'),
    path('resources/delete/<int:resource_id>/', delete_resource, name='delete_resource'),
    path('logout/', views.custom_logout, name='logout'),
    # New instructor features
    path('course/create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('student/<int:student_id>/detail/', views.student_detail, name='student_detail'),
]
