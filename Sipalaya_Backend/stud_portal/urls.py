
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='stud_dashboard'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_completed, name='mark_lesson_completed'),
    path('assignments/submit/<int:course_id>/', views.submit_assignment, name='submit_assignment'),
    path('assignments/view/', views.view_assignments, name='view_assignments'),
    path('attendance/', views.view_attendance, name='view_attendance'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
]
