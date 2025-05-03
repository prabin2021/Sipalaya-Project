from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<int:course_id>/', views.initiate_payment, name='initiate_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('installment/<int:plan_id>/', views.installment_details, name='installment_details'),
]