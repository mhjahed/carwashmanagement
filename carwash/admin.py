from django.contrib import admin
from .models import ServiceType, Customer, Ticket, Event


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'email')
    ordering = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'car_number', 'customer', 'service_type', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'service_type', 'created_at')
    search_fields = ('ticket_id', 'car_number', 'customer__name', 'customer__phone')
    readonly_fields = ('ticket_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('ticket_id', 'car_number', 'car_model', 'service_type', 'customer')
        }),
        ('Status & Payment', {
            'fields': ('status', 'payment_status', 'assigned_to')
        }),
        ('Pricing', {
            'fields': ('service_price', 'additional_charges', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_urgent', 'is_active', 'created_at', 'created_by')
    list_filter = ('priority', 'is_urgent', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'priority', 'is_urgent', 'is_active')
        }),
        ('Target Audience', {
            'fields': ('target_roles',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'event_date'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
