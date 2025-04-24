from django.contrib import admin
from .models import Banner, Feature, Testimonial, FAQ, Contact, SiteSetting

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    ordering = ('order',)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'company', 'rating', 'is_active', 'order')
    list_filter = ('is_active', 'rating')
    search_fields = ('name', 'role', 'company', 'content')
    ordering = ('order',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'created_at')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    ordering = ('category', 'order')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of SiteSetting
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request) 