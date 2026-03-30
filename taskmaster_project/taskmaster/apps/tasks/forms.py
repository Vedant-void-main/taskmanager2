from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'due_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'What needs to be done?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Add details (optional)...'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
