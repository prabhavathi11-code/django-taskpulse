from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import Task
from .forms import TaskForm

@require_http_methods(["GET"])
def task_list(request):
    tasks = Task.objects.all()

    # Search filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Status filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter and status_filter in Task.Status.values:
        tasks = tasks.filter(status=status_filter)

    # Priority filter
    priority_filter = request.GET.get('priority', '').strip()
    if priority_filter and priority_filter in Task.Priority.values:
        tasks = tasks.filter(priority=priority_filter)

    # Category filter
    category_filter = request.GET.get('category', '').strip()
    if category_filter and category_filter in Task.Category.values:
        tasks = tasks.filter(category=category_filter)

    # Calculate overall dashboard metrics
    all_tasks = Task.objects.all()
    total_count = all_tasks.count()
    completed_count = all_tasks.filter(status=Task.Status.COMPLETED).count()
    pending_count = all_tasks.filter(status=Task.Status.PENDING).count()
    in_progress_count = all_tasks.filter(status=Task.Status.IN_PROGRESS).count()
    high_priority_count = all_tasks.filter(priority=Task.Priority.HIGH).count()
    completion_rate = int((completed_count / total_count * 100)) if total_count > 0 else 0

    form = TaskForm()

    context = {
        'tasks': tasks,
        'total_count': total_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'high_priority_count': high_priority_count,
        'completion_rate': completion_rate,
        'search_query': search_query,
        'selected_status': status_filter,
        'selected_priority': priority_filter,
        'selected_category': category_filter,
        'form': form,
        'categories': Task.Category.choices,
        'priorities': Task.Priority.choices,
        'statuses': Task.Status.choices,
    }
    return render(request, 'tasks/task_list.html', context)

@require_http_methods(["GET", "POST"])
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('tasks:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@require_http_methods(["GET", "POST"])
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect('tasks:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task, 'action': 'Edit'})

@require_http_methods(["GET", "POST"])
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" was deleted.')
        return redirect('tasks:list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.status == Task.Status.COMPLETED:
        task.status = Task.Status.PENDING
    else:
        task.status = Task.Status.COMPLETED
    task.save()
    messages.info(request, f'Status updated for "{task.title}".')
    return redirect('tasks:list')

@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'app': 'TaskPulse Django',
        'database': 'connected',
        'total_tasks': Task.objects.count()
    })

