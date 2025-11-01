from django import forms
from .models import EmployerRequest, RequestReply


class EmployerRequestForm(forms.ModelForm):
    """Form for creating employer requests."""
    
    class Meta:
        model = EmployerRequest
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Request Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your request...'}),
        }


class RequestReplyForm(forms.ModelForm):
    """Form for replying to requests."""
    
    class Meta:
        model = RequestReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type your reply...'}),
        }
