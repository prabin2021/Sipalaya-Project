from django.contrib import admin
from .models import Banner, Feature
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'date_submitted')  # Display phone number
    search_fields = ('name', 'email', 'phone_number')  # Add phone number to search
    list_filter = ('date_submitted',)  # Filter submissions by date

admin.site.register(Banner)
admin.site.register(Feature)
