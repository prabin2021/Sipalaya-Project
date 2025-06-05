from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('placement-services/', views.placement_services, name='placement_services'),
    path('job-listings/', views.job_listings, name='job_listings'),
    path('job-listings/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('alumni-stories/', views.alumni_stories, name='alumni_stories'),
] 