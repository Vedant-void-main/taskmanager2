from django.db import models
from django.contrib.auth.models import User  # Built-in User model


class Task(models.Model):
    # Link each task to a specific user
    # If the user is deleted, their tasks are also deleted (CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Task details
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Optional field
    date        = models.DateField()
    time        = models.TimeField()

    # Status: is the task done or not?
    is_completed = models.BooleanField(default=False)

    # Automatically saved when the task is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # This shows up in Django admin
        return f"{self.title} — {self.user.username}"

    class Meta:
        # Show newest tasks first
        ordering = ['-created_at']
