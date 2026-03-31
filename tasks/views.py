from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from .forms import SignupForm, TaskForm


# ----- Signup View -----
def signup_view(request):
    """Handles new user registration."""

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()          # Save user to database
            login(request, user)        # Log them in right away
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


# ----- Dashboard View -----
@login_required   # User must be logged in to access this
def dashboard(request):
    """Shows task summary and the task list with filter options."""

    # Get only this user's tasks
    all_tasks = Task.objects.filter(user=request.user)

    # Read the filter from the URL query string (?filter=completed)
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'completed':
        tasks = all_tasks.filter(is_completed=True)

    elif filter_type == 'pending':
        tasks = all_tasks.filter(is_completed=False)

    elif filter_type == 'today':
        today = timezone.localdate()  # Get today's date in the configured timezone
        tasks = all_tasks.filter(date=today)

    else:
        tasks = all_tasks  # Show all tasks by default

    # Calculate statistics for the summary cards
    total     = all_tasks.count()
    completed = all_tasks.filter(is_completed=True).count()
    pending   = all_tasks.filter(is_completed=False).count()

    # Avoid division by zero
    if total > 0:
        percentage = round((completed / total) * 100)
    else:
        percentage = 0

    context = {
        'tasks':       tasks,
        'total':       total,
        'completed':   completed,
        'pending':     pending,
        'percentage':  percentage,
        'filter_type': filter_type,   # So we can highlight the active filter button
    }

    return render(request, 'dashboard.html', context)


# ----- Add Task View -----
@login_required
def add_task(request):
    """Handles adding a new task."""

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Don't save to DB yet
            task.user = request.user        # Attach the logged-in user
            task.save()                     # Now save to DB
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'tasks/add_task.html', {'form': form})


# ----- Mark Task as Complete -----
@login_required
def mark_complete(request, pk):
    """Toggles a task between completed and pending."""

    # Make sure the task belongs to this user
    task = get_object_or_404(Task, pk=pk, user=request.user)

    # Toggle the status
    task.is_completed = not task.is_completed
    task.save()

    return redirect('dashboard')


# ----- Delete Task -----
@login_required
def delete_task(request, pk):
    """Deletes a task after confirming it belongs to the user."""

    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    # Show a confirmation page before deleting
    return render(request, 'tasks/confirm_delete.html', {'task': task})
