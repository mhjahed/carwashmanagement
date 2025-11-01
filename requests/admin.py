from django.contrib import admin
from .models import EmployerRequest, RequestReply


class RequestReplyInline(admin.TabularInline):
    model = RequestReply
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EmployerRequest)
class EmployerRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'request_type', 'is_instruction', 'is_active', 'is_read', 'created_at')
    list_filter = ('request_type', 'is_instruction', 'is_active', 'is_read', 'created_at')
    search_fields = ('title', 'content', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    inlines = [RequestReplyInline]
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'title', 'content', 'request_type', 'is_instruction')
        }),
        ('Status', {
            'fields': ('is_active', 'is_read')
        }),
    )


@admin.register(RequestReply)
class RequestReplyAdmin(admin.ModelAdmin):
    list_display = ('request', 'author', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('content', 'request__title', 'author__first_name', 'author__last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Reply Information', {
            'fields': ('request', 'author', 'content')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )
