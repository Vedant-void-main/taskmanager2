from django import forms
from .models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'reminder_type', 'date', 'time', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Person's name or event title"
            }),
            'reminder_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2, 'placeholder': 'Optional notes...'
            }),
        }
