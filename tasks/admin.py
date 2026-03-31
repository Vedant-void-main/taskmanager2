from django.contrib import admin
from .models import Task

# Register Task model so it appears in the admin panel
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'time', 'is_completed')
    list_filter  = ('is_completed', 'date')
    search_fields = ('title', 'user__username')
