from django import forms
from .models import EmployerAttendance, EmployerNote
from accounts.models import User


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance."""
    
    class Meta:
        model = EmployerAttendance
        fields = ['status', 'check_in_time', 'check_out_time', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class EmployerNoteForm(forms.ModelForm):
    """Form for creating employer notes."""
    
    class Meta:
        model = EmployerNote
        fields = ['employer', 'title', 'content', 'is_important']
        widgets = {
            'employer': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Note content...'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to only show employers
        self.fields['employer'].queryset = User.objects.filter(role='employer')
