from django.urls import path
from . import views

app_name = 'testimonials'

urlpatterns = [
    path('', views.testimonial_list, name='testimonial_list'),
    path('add/<int:course_id>/', views.add_testimonial, name='add_testimonial'),
    path('review/add/<int:course_id>/', views.add_review, name='add_review'),
    path('reviews/<int:course_id>/', views.get_course_reviews, name='get_course_reviews'),
] 