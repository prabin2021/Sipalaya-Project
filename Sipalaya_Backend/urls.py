from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('courses/', include('courses.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('stud_portal/', include('stud_portal.urls')),
    path('blog/', include('blog.urls')),
    path('payments/', include('payments.urls')),
    path('demo-classes/', include('demo_classes.urls', namespace='demo_classes')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)