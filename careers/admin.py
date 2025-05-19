from django.contrib import admin
from .models import PlacementService, CompanyPartnership, JobListing, AlumniSuccessStory

@admin.register(PlacementService)
class PlacementServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'created_at')
    search_fields = ('title', 'description')

@admin.register(CompanyPartnership)
class CompanyPartnershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at')
    search_fields = ('name', 'description')

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'application_deadline', 'is_active')
    list_filter = ('job_type', 'is_active', 'application_deadline')
    search_fields = ('title', 'description', 'requirements', 'company__name')

@admin.register(AlumniSuccessStory)
class AlumniSuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'graduation_year', 'current_position', 'company')
    list_filter = ('graduation_year',)
    search_fields = ('name', 'current_position', 'company', 'story')
