from django.contrib import admin
from .models import PaymentMethod, Payment, InstallmentPlan

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'name')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'student', 'course', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'is_installment', 'payment_date')
    search_fields = ('transaction_id', 'student__username', 'student__email', 'course__title')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'course', 'amount', 'payment_method', 'transaction_id', 'status')
        }),
        ('Installment Information', {
            'fields': ('is_installment', 'installment_number', 'total_installments'),
            'classes': ('collapse',)
        }),
        ('Refund Information', {
            'fields': ('refund_amount', 'refund_date', 'refund_reason'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('payment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(InstallmentPlan)
class InstallmentPlanAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'total_amount', 'number_of_installments', 'amount_per_installment', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('student__username', 'student__email', 'course__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'course', 'total_amount', 'number_of_installments', 'amount_per_installment')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
