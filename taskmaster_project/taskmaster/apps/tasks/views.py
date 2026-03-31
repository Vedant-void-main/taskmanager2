from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from .models import Task
from .forms import TaskForm
from apps.reminders.models import Reminder


@login_required
def dashboard(request):
    today = timezone.now().date()
    tasks = Task.objects.filter(user=request.user)
    total = tasks.count()
    completed = tasks.filter(status='completed').count()
    pending = tasks.filter(status='pending').count()
    overdue = tasks.filter(status='pending', due_date__lt=today).count()

    recent_tasks = tasks.filter(status='pending').order_by('due_date')[:5]

    upcoming_reminders = Reminder.objects.filter(
        user=request.user
    ).order_by('date')[:5]

    today_reminders = []
    for r in Reminder.objects.filter(user=request.user):
        if r.is_today:
            today_reminders.append(r)

    context = {
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'recent_tasks': recent_tasks,
        'upcoming_reminders': upcoming_reminders,
        'today_reminders': today_reminders,
        'completion_pct': round((completed / total * 100) if total > 0 else 0),
        'page': 'dashboard',
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_list(request):
    filter_status = request.GET.get('filter', 'all')
    filter_priority = request.GET.get('priority', 'all')
    tasks = Task.objects.filter(user=request.user)

    if filter_status == 'completed':
        tasks = tasks.filter(status='completed')
    elif filter_status == 'pending':
        tasks = tasks.filter(status='pending')

    if filter_priority in ['low', 'medium', 'high']:
        tasks = tasks.filter(priority=filter_priority)

    form = TaskForm()
    context = {
        'tasks': tasks,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
        'form': form,
        'page': 'tasks',
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'✅ Task "{task.title}" created!')
            return redirect('task_list')
        else:
            messages.error(request, 'Please fix the errors.')
    return redirect('task_list')


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'✏️ Task "{task.title}" updated!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task, 'page': 'tasks'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'🗑️ Task "{title}" deleted.')
    return redirect('task_list')


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.status = 'completed' if task.status == 'pending' else 'pending'
        task.save()
        return JsonResponse({'status': task.status, 'title': task.title})
    return JsonResponse({'error': 'Invalid'}, status=400)


@login_required
def check_notifications(request):
    """AJAX endpoint polled every 60s by the frontend."""
    today = timezone.now().date()
    now = timezone.now()
    alerts = []

    # Overdue tasks
    overdue = Task.objects.filter(user=request.user, status='pending', due_date__lt=today)
    for t in overdue:
        alerts.append({
            'type': 'danger',
            'icon': '⚠️',
            'title': 'Overdue Task',
            'message': f'"{t.title}" was due on {t.due_date.strftime("%b %d")}',
        })

    # Due today
    due_today = Task.objects.filter(user=request.user, status='pending', due_date=today)
    for t in due_today:
        alerts.append({
            'type': 'warning',
            'icon': '⏰',
            'title': 'Due Today',
            'message': f'"{t.title}" is due today!',
        })

    # Today's reminders
    for r in Reminder.objects.filter(user=request.user):
        if r.is_today:
            icon = {'birthday': '🎂', 'anniversary': '💍', 'custom': '🔔'}.get(r.reminder_type, '🔔')
            alerts.append({
                'type': 'info',
                'icon': icon,
                'title': r.get_reminder_type_display(),
                'message': f'{r.title} is today!',
            })

    return JsonResponse({'alerts': alerts})
