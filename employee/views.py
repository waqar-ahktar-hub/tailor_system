"""Views for order application."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import View

from employee.forms import EmployeeForm
from employee.models import Employee
from order.models import Task


class EmployeeListView(LoginRequiredMixin, View):
    """List all employees."""

    def _get_employee_with_tasks(self, employees):
        """Get employees against number and status of tasks."""
        task_groupby_employee = Task.objects.all().values('employee').annotate(total=Count('employee'))
        employee_with_no_of_tasks = {}
        for employee in employees:
            tasks = Task.objects.filter(employee=employee)
            total_task_count = tasks.count()
            pending_task_count = tasks.exclude(status=Task.COMPLETED).count()
            percent_complete = 0
            if total_task_count > 0:
                percent_complete = round(((total_task_count - pending_task_count)/total_task_count) * 100, 2)
            completed_task_count = total_task_count - pending_task_count
            employee_with_no_of_tasks[employee.id] = (
                total_task_count,
                pending_task_count,
                percent_complete,
                completed_task_count
            )
        return employee_with_no_of_tasks

    def get(self, request):
        """Render employee list template.."""
        employees = Employee.objects.all().order_by('name')

        employee_with_no_of_tasks = self._get_employee_with_tasks(employees)

        context = {
            'employees': employees,
            'employee_with_no_of_tasks': employee_with_no_of_tasks
        }
        return render(request, 'employee/list-employees.html', context)

    def post(self, request):
        """Render employee list template.."""
        query = request.POST.get('search_query')
        employees = Employee.objects.all().order_by('name')

        if query:
            employees = employees.filter(
                Q(name__icontains=query)
                | Q(phone_number__icontains=query)
            )

        employee_with_no_of_tasks = self._get_employee_with_tasks(employees)

        context = {
            'employees': employees,
            'employee_with_no_of_tasks': employee_with_no_of_tasks,
            'query': query
        }
        return render(request, 'employee/list-employees.html', context)


employee_list_view = EmployeeListView.as_view()


class EmployeeDetailView(LoginRequiredMixin, View):
    """Class based view for Employee for detail of Employee."""

    def get(self, request, id):
        """Render Employee detail tempalte.."""
        employee = Employee.objects.get(id=id)
        context = {
            'employee': employee,
            'tasks': Task.objects.filter(employee=employee)
        }
        return render(request, 'employee/employee-detail.html', context)


employee_detail_view = EmployeeDetailView.as_view()


class EmployeeAddView(LoginRequiredMixin, View):
    """Class based view for adding new Employee."""

    def get(self, request):
        """Return add new Employee form."""
        form = EmployeeForm()
        return render(request, 'employee/add-employee.html',
                      {'form': form, 'func': 'Add'})

    def post(self, request):
        """Save employee and redirect to employee list."""
        form = EmployeeForm(request.POST)
        if form.is_valid():
            new_employee = form.save()
            return redirect('employee:employee_detail', id=new_employee.id)
        else:
            return render(request, 'employee/add-employee.html', {'form': form, 'func': 'Add'})


employee_add_view = EmployeeAddView.as_view()


class EmployeeUpdateView(LoginRequiredMixin, View):
    """Class based view for adding new Employee."""

    def get(self, request, id):
        """Return add new Employee form."""
        employee = get_object_or_404(Employee, id=id)
        form = EmployeeForm(instance=employee)
        return render(request, 'employee/add-employee.html',
                      {'form': form, 'func': 'Update', 'employee': employee})

    def post(self, request, id):
        """Save employee and redirect to employee list."""
        employee = get_object_or_404(Employee, id=id)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            new_employee = form.save()
            return redirect('employee:employee_detail', id=new_employee.id)
        else:
            return render(request, 'employee/add-employee.html', {'form': form, 'func': 'Update', 'employee': employee})


employee_update_view = EmployeeUpdateView.as_view()


class EmployeeDeleteView(LoginRequiredMixin, View):
    """Class based view for deleting Employee."""

    def post(self, request):
        """Delete employee."""
        id = request.POST.get('id')
        employee = get_object_or_404(Employee, id=id)
        employee.delete()
        return redirect('employee:employees')


employee_delete_view = EmployeeDeleteView.as_view()
