from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.enrolled_courses, name='enrolled_courses'),
    path('course/<slug:slug>/', views.course_content, name='course_content'),
    path('course/<slug:slug>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('course/<slug:slug>/lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('course/<slug:slug>/review/', views.add_review, name='add_review'),
    path('course/<slug:slug>/review/edit/', views.edit_review, name='edit_review'),
    path('course/<slug:slug>/progress/', views.course_progress, name='course_progress'),
] 