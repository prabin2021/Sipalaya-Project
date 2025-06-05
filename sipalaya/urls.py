from django.urls import path, include

urlpatterns = [
    path('courses/', include('courses.urls')),
    path('blog/', include('blog.urls')),
    path('feedback/', include('feedback.urls')),
] 