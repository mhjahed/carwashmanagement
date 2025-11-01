from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from accounts.models import User


class ServiceType(models.Model):
    """Service types with configurable pricing."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ৳{self.price}"
    
    class Meta:
        verbose_name = 'Service Type'
        verbose_name_plural = 'Service Types'
        ordering = ['name']


class Customer(models.Model):
    """Customer information."""
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.phone})"
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['name']


class Ticket(models.Model):
    """Car wash ticket with auto-generated ID."""
    
    STATUS_CHOICES = [
        ('under_working', 'Under Working'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('due', 'Due'),
        ('paid', 'Paid'),
    ]
    
    # Auto-generated ticket ID
    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Car information
    car_number = models.CharField(max_length=20)
    car_model = models.CharField(max_length=100, blank=True)
    
    # Service and customer
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    # Status and payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_working')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='due')
    
    # Pricing
    service_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Assigned employer
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   limit_choices_to={'role': 'employer'})
    
    def __str__(self):
        return f"Ticket #{self.ticket_id} - {self.car_number}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            # Generate auto ticket ID
            today = timezone.now().date()
            date_str = today.strftime('%Y%m%d')
            
            # Get the last ticket for today
            last_ticket = Ticket.objects.filter(
                ticket_id__startswith=date_str
            ).order_by('-ticket_id').first()
            
            if last_ticket:
                # Extract the number and increment
                last_number = int(last_ticket.ticket_id[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.ticket_id = f"{date_str}{new_number:04d}"
        
        # Calculate total amount
        self.total_amount = self.service_price + self.additional_charges
        
        super().save(*args, **kwargs)
    
    @property
    def is_completed(self):
        return self.status == 'completed'
    
    @property
    def is_paid(self):
        return self.payment_status == 'paid'
    
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created_at']


class Event(models.Model):
    """Events and urgent notices from SuperAdmin."""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    is_urgent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Target audience
    target_roles = models.JSONField(default=list, help_text="List of roles this event is for")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_date = models.DateTimeField(null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  limit_choices_to={'role': 'superadmin'})
    
    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-created_at']
