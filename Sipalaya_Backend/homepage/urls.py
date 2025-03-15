from django.urls import path
from .views import homepage_view, search_view
from django.contrib.auth import views as auth_views
from . import views  

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('', search_view, name='search_courses'),
    path('about/', views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('protected/', views.protected_page, name='protected_page'),
]

