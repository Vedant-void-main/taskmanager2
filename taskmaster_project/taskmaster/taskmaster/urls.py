from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('users/', include('apps.users.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('reminders/', include('apps.reminders.urls')),
    path('dashboard/', include('apps.tasks.dashboard_urls')),
]
