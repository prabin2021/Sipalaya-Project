from django.urls import path
from .views import course_list, course_detail, courses_by_category

urlpatterns = [
    path('', course_list, name='course_list'),
    path('<int:course_id>/', course_detail, name='course_detail'),
    path('category/<int:category_id>/', courses_by_category, name='courses_by_category'),
]
