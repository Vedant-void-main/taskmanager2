from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Reminder(models.Model):
    TYPE_CHOICES = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('custom', 'Custom Event'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    reminder_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='custom')
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} ({self.get_reminder_type_display()})"

    @property
    def is_today(self):
        today = timezone.now().date()
        # Match month and day (recurring yearly events)
        return self.date.month == today.month and self.date.day == today.day

    @property
    def days_until(self):
        today = timezone.now().date()
        # Next occurrence this year or next
        this_year = self.date.replace(year=today.year)
        if this_year < today:
            this_year = self.date.replace(year=today.year + 1)
        return (this_year - today).days

    @property
    def type_icon(self):
        return {'birthday': '🎂', 'anniversary': '💍', 'custom': '🔔'}.get(self.reminder_type, '🔔')

    @property
    def type_color(self):
        return {'birthday': 'pink', 'anniversary': 'purple', 'custom': 'blue'}.get(self.reminder_type, 'blue')
