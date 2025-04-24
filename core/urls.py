from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('instructor/dashboard/', views.InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
] 