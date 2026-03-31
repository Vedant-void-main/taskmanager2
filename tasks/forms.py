from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


# ----- Signup Form -----
class SignupForm(UserCreationForm):
    # Add email field to the default signup form
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ----- Add Task Form -----
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Don't include 'user' or 'is_completed' — we set those in the view
        fields = ['title', 'description', 'date', 'time']

        # Customize input types for date and time pickers
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
