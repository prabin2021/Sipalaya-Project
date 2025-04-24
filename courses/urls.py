from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
    path('<slug:slug>/learn/', views.CourseLearnView.as_view(), name='course_learn'),
    path('<slug:slug>/review/', views.CourseReviewView.as_view(), name='course_review'),
    
    # Instructor URLs
    path('instructor/courses/', views.InstructorCourseListView.as_view(), name='instructor_course_list'),
    path('instructor/courses/create/', views.InstructorCourseCreateView.as_view(), name='instructor_course_create'),
    path('instructor/courses/<int:pk>/update/', views.InstructorCourseUpdateView.as_view(), name='instructor_course_update'),
    path('instructor/courses/<int:pk>/delete/', views.InstructorCourseDeleteView.as_view(), name='instructor_course_delete'),
] 