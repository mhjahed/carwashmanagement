from django.db import models
from django.utils import timezone
from accounts.models import User


class EmployerAttendance(models.Model):
    """Employer attendance tracking."""
    
    STATUS_CHOICES = [
        ('worked', 'Worked'),
        ('missed', 'Missed'),
        ('leave', 'Leave'),
        ('half_day', 'Half Day'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'})
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='worked')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date} ({self.get_status_display()})"
    
    class Meta:
        verbose_name = 'Employer Attendance'
        verbose_name_plural = 'Employer Attendances'
        unique_together = ('user', 'date')
        ordering = ['-date']


class EmployerNote(models.Model):
    """Private notes from Author to Employer."""
    
    employer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'}, related_name='notes_received')
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'author'}, related_name='notes_created')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_important = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.employer.get_full_name()}"
    
    class Meta:
        verbose_name = 'Employer Note'
        verbose_name_plural = 'Employer Notes'
        ordering = ['-created_at']
