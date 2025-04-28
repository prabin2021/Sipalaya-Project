from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_completed, name='mark_lesson_completed'),
    path('assignments/submit/<int:course_id>/', views.submit_assignment, name='submit_assignment'),
    path('assignments/', views.view_assignments, name='view_assignments'),
    path('attendance/', views.view_attendance, name='view_attendance'),
]
