from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks import views as task_views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Auth pages - using Django's built-in views
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(),                            name='logout'),

    # Signup page - our custom view
    path('signup/', task_views.signup_view, name='signup'),

    # Dashboard
    path('dashboard/', task_views.dashboard, name='dashboard'),

    # Task actions
    path('tasks/add/',              task_views.add_task,     name='add_task'),
    path('tasks/complete/<int:pk>/', task_views.mark_complete, name='mark_complete'),
    path('tasks/delete/<int:pk>/',  task_views.delete_task,  name='delete_task'),
]
