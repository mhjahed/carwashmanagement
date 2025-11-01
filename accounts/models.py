from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with role-based access control."""
    
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('author', 'Author'),
        ('superadmin', 'SuperAdmin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employer')
    phone = models.CharField(max_length=15, blank=True)
    post = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_employer(self):
        return self.role == 'employer'
    
    def is_author(self):
        return self.role == 'author'
    
    def is_superadmin(self):
        return self.role == 'superadmin'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
