from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reminder
from .forms import ReminderForm


@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(user=request.user)
    filter_type = request.GET.get('type', 'all')
    if filter_type in ['birthday', 'anniversary', 'custom']:
        reminders = reminders.filter(reminder_type=filter_type)

    # Sort by days_until
    reminders = sorted(reminders, key=lambda r: r.days_until)

    form = ReminderForm()
    context = {
        'reminders': reminders,
        'filter_type': filter_type,
        'form': form,
        'page': 'reminders',
    }
    return render(request, 'reminders/reminder_list.html', context)


@login_required
def reminder_create(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, f'{reminder.type_icon} Reminder "{reminder.title}" added!')
            return redirect('reminder_list')
        else:
            messages.error(request, 'Please fix the errors.')
    return redirect('reminder_list')


@login_required
def reminder_edit(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            messages.success(request, f'✏️ Reminder "{reminder.title}" updated!')
            return redirect('reminder_list')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'reminders/reminder_edit.html', {
        'form': form, 'reminder': reminder, 'page': 'reminders'
    })


@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        title = reminder.title
        reminder.delete()
        messages.success(request, f'🗑️ Reminder "{title}" deleted.')
    return redirect('reminder_list')
