"""Views for order application."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import View

from order.forms import TaskForm
from order.models import Order, Task


class TaskListView(LoginRequiredMixin, View):
    """Class based view for Order for listing all the orders."""

    def get(self, request):
        """Render task list template.."""
        tasks = Task.objects.all()
        context = {
            'tasks': tasks,
        }
        return render(request, 'task/list-tasks.html', context)


task_list_view = TaskListView.as_view()


class TaskDetailView(LoginRequiredMixin, View):
    """Class based view for tasks for detail of tasks."""

    def get(self, request, id):
        """Render tasks detail tempalte.."""
        task = Task.objects.get(id=id)
        context = {
            'task': task,
        }
        return render(request, 'task/task-detail.html', context)


task_detail_view = TaskDetailView.as_view()


class TaskAddView(LoginRequiredMixin, View):
    """Class based view for adding new task."""

    def get(self, request, order_id):
        """Return add new task form."""
        order = get_object_or_404(Order, id=order_id)
        form = TaskForm()
        return render(request, 'task/add-task.html',
                      {'form': form, 'func': 'Add', 'order': order})

    def post(self, request, order_id):
        """Save task and redirect to task list."""
        form = TaskForm(request.POST)
        order = get_object_or_404(Order, id=order_id)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.order = order
            new_task.save()
            return redirect('order:tasks')
        else:
            return render(request, 'task/add-task.html', {'form': form, 'func': 'Add', 'order': order})


task_add_view = TaskAddView.as_view()


class TaskUpdateView(LoginRequiredMixin, View):
    """Class based view for updating new task."""

    def get(self, request, id):
        """Return add new task form."""
        task = get_object_or_404(Task, id=id)
        form = TaskForm(instance=task)
        return render(request, 'task/add-task.html',
                      {'form': form, 'func': 'Update', 'task': task})

    def post(self, request, id):
        """Save order and redirect to task list."""
        task = get_object_or_404(Task, id=id)
        order = get_object_or_404(Order, id=task.order.id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.order = order
            new_task.save()
            return redirect('order:tasks')
        else:
            return render(request, 'task/add-task.html', {'form': form, 'func': 'Update', 'task': task})


task_update_view = TaskUpdateView.as_view()


class TaskDeleteView(LoginRequiredMixin, View):
    """Class based view for tasks for deletion of task."""

    def post(self, request):
        """Render task list tempalte after deletion."""
        id = request.POST.get('id')
        task = get_object_or_404(Task, id=id)
        task.delete()
        return redirect('order:tasks')


task_delete_view = TaskDeleteView.as_view()
