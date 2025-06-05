from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # List and Dashboard views
    path('', views.course_list, name='course_list'),
    path('category/<slug:category_slug>/', views.course_list, name='course_list_by_category'),
    
    # Payment related URLs
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    path('installments/', views.installment_payments, name='installment_payments'),
    path('installments/<int:payment_id>/pay/', views.pay_installment, name='pay_installment'),
    
    # Course content URLs
    path('<slug:slug>/content/', views.course_content, name='course_content'),
    path('<slug:slug>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:slug>/payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('<slug:slug>/progress/', views.course_progress, name='course_progress'),
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    
    # Assignment URLs
    path('assignments/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('demo-class/<int:demo_class_id>/book/', views.book_demo_class, name='book_demo_class'),
    
    # Dashboard
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Course detail (keep this last as it's the most generic)
    path('<slug:slug>/', views.course_detail, name='course_detail'),
] 