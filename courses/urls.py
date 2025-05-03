from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('category/<int:category_id>/', views.courses_by_category, name='courses_by_category'),
    path('search/', views.search_courses, name='search_courses'),
    path('demo-class/', views.demo_class_schedule, name='demo_class_schedule'),
    path('demo-class/<int:course_id>/', views.demo_class_schedule, name='demo_class_schedule'),
    path('demo-class/register/<int:demo_class_id>/', views.register_demo_class, name='register_demo_class'),
    path('payment/<int:course_id>/', views.payment_page, name='payment_page'),
    path('payment/process/<int:course_id>/', views.process_payment, name='process_payment'),
    path('payment/esewa/success/', views.esewa_success, name='esewa_success'),
    path('payment/esewa/failure/', views.esewa_failure, name='esewa_failure'),
    path('resources/<int:course_id>/', views.manage_course_resources, name='manage_course_resources'),
    path('resources/<int:course_id>/upload/', views.upload_resource, name='upload_resource'),
    path('resources/<int:resource_id>/delete/', views.delete_resource, name='delete_resource'),
]
