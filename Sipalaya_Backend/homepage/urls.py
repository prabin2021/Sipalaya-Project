from django.urls import path
from .views import homepage_view, search_view

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('search/', search_view, name='search_courses'),
]
