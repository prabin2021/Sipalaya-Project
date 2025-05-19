from django.contrib import admin
from .models import Banner, Testimonial, Statistic, Service, CompanyInfo, Milestone, TeamMember, Partnership, Certification, Contact, AlumniSuccessStory

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'order')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'subtitle')
    ordering = ('order', '-created_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'image', 'button_text')
        }),
        ('Category', {
            'fields': ('category',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'position', 'rating', 'is_active')
    list_filter = ('is_active', 'rating')
    search_fields = ('name', 'company', 'content')
    ordering = ('-created_at',)

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'icon', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('order',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['established_date']
    
    def has_add_permission(self, request):
        # Only allow one instance of CompanyInfo
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'order']
    list_editable = ['order']
    search_fields = ['title', 'description']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'designation', 'is_key_member', 'order']
    list_editable = ['order', 'is_key_member']
    list_filter = ['role', 'is_key_member']
    search_fields = ['name', 'designation', 'bio']

@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_active', 'partnership_date', 'order']
    list_editable = ['order', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'description']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'validity_period', 'is_featured']
    list_editable = ['is_featured']
    list_filter = ['provider', 'is_featured']
    search_fields = ['name', 'description']
