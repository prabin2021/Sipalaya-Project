from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/add/', views.add_testimonial, name='add_testimonial'),
    path('course/<slug:course_slug>/review/', views.add_review, name='add_review'),
] 