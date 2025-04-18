
from django.urls import path
from . import views
from .views import register_view
urlpatterns = [
    path('register/', register_view, name='register'),
    path('dashboard/', views.role_based_dashboard, name='dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_completed, name='mark_lesson_completed'),
    path('assignments/submit/<int:course_id>/', views.submit_assignment, name='submit_assignment'),
    path('assignments/view/', views.view_assignments, name='view_assignments'),
    path('attendance/', views.view_attendance, name='view_attendance'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
]
