from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('course/<slug:slug>/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('list/', views.PaymentListView.as_view(), name='payment_list'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('<int:payment_id>/refund/', views.RefundCreateView.as_view(), name='refund_create'),
    path('refunds/', views.RefundListView.as_view(), name='refund_list'),
] 