from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.due_date and self.status == 'pending':
            return self.due_date < timezone.now().date()
        return False

    @property
    def is_due_soon(self):
        if self.due_date and self.status == 'pending':
            delta = self.due_date - timezone.now().date()
            return 0 <= delta.days <= 1
        return False

    @property
    def priority_color(self):
        return {'low': 'success', 'medium': 'warning', 'high': 'danger'}.get(self.priority, 'secondary')

    @property
    def priority_icon(self):
        return {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(self.priority, '⚪')
