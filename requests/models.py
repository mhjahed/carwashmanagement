from django.db import models
from django.utils import timezone
from accounts.models import User


class EmployerRequest(models.Model):
    """Employer requests and Author instructions."""
    
    REQUEST_TYPE_CHOICES = [
        ('request', 'Request'),
        ('instruction', 'Instruction'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'})
    title = models.CharField(max_length=200)
    content = models.TextField()
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, default='request')
    is_instruction = models.BooleanField(default=False, help_text="If True, this is an instruction from Author")
    is_active = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"
    
    class Meta:
        verbose_name = 'Employer Request'
        verbose_name_plural = 'Employer Requests'
        ordering = ['-created_at']


class RequestReply(models.Model):
    """Replies to employer requests."""
    
    request = models.ForeignKey(EmployerRequest, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'author'})
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reply to: {self.request.title}"
    
    class Meta:
        verbose_name = 'Request Reply'
        verbose_name_plural = 'Request Replies'
        ordering = ['created_at']
