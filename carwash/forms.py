from django import forms
from .models import ServiceType, Customer, Ticket


class CustomerForm(forms.ModelForm):
    """Form for creating/updating customers."""
    
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
        }


class TicketForm(forms.ModelForm):
    """Form for creating/updating tickets."""
    
    # Customer fields for inline editing
    customer_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    customer_phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    customer_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    customer_address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    
    class Meta:
        model = Ticket
        fields = ['car_number', 'car_model', 'service_type', 'assigned_to', 'additional_charges']
        widgets = {
            'car_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Car Number'}),
            'car_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Car Model'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'additional_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter assigned_to to only show employers
        self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(role='employer')
        
        # If editing existing ticket, populate customer fields
        if self.instance and self.instance.pk:
            self.fields['customer_name'].initial = self.instance.customer.name
            self.fields['customer_phone'].initial = self.instance.customer.phone
            self.fields['customer_email'].initial = self.instance.customer.email
            self.fields['customer_address'].initial = self.instance.customer.address
    
    def save(self, commit=True):
        ticket = super().save(commit=False)
        
        # Get or create customer
        customer_name = self.cleaned_data['customer_name']
        customer_phone = self.cleaned_data['customer_phone']
        customer_email = self.cleaned_data['customer_email']
        customer_address = self.cleaned_data['customer_address']
        
        customer, created = Customer.objects.get_or_create(
            name=customer_name,
            defaults={
                'phone': customer_phone,
                'email': customer_email,
                'address': customer_address,
            }
        )
        
        # Update customer if not created
        if not created:
            customer.phone = customer_phone
            customer.email = customer_email
            customer.address = customer_address
            customer.save()
        
        ticket.customer = customer
        ticket.service_price = ticket.service_type.price
        
        if commit:
            ticket.save()
        
        return ticket


class TicketUpdateForm(forms.ModelForm):
    """Form for updating ticket status and payment."""
    
    class Meta:
        model = Ticket
        fields = ['status', 'payment_status', 'assigned_to', 'additional_charges']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'additional_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter assigned_to to only show employers
        self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(role='employer')
    
    def save(self, commit=True):
        ticket = super().save(commit=False)
        
        # Set completion time if status changed to completed
        if ticket.status == 'completed' and not ticket.completed_at:
            from django.utils import timezone
            ticket.completed_at = timezone.now()
        
        if commit:
            ticket.save()
        
        return ticket
