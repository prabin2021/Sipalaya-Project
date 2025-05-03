from django.urls import path
from . import views

app_name = 'demo_classes'

urlpatterns = [
    # Public views
    path('', views.demo_class_list, name='list'),
    path('<int:demo_class_id>/', views.demo_class_detail, name='detail'),
    path('schedule/<int:schedule_id>/book/', views.book_demo_class, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('feedback/<int:booking_id>/', views.submit_feedback, name='submit_feedback'),
    
    # Admin views
    path('create/', views.create_demo_class, name='create'),
    path('<int:demo_class_id>/create-schedule/', views.create_schedule, name='create_schedule'),
] 