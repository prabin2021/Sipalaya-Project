from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('profile/password/', views.change_password, name='change_password'),
] 