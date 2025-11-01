from django.contrib import admin
from .models import EmployerAttendance, EmployerNote


@admin.register(EmployerAttendance)
class EmployerAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status', 'check_in_time', 'check_out_time', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    ordering = ('-date',)
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('user', 'date', 'status')
        }),
        ('Time Tracking', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(EmployerNote)
class EmployerNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'author', 'is_important', 'is_read', 'created_at')
    list_filter = ('is_important', 'is_read', 'created_at')
    search_fields = ('title', 'content', 'employer__first_name', 'employer__last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Note Information', {
            'fields': ('employer', 'author', 'title', 'content')
        }),
        ('Status', {
            'fields': ('is_important', 'is_read')
        }),
    )
