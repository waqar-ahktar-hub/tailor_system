"""urls for employee application."""

from django.urls import path

from employee.views import (
    employee_add_view,
    employee_delete_view,
    employee_detail_view,
    employee_list_view,
    employee_update_view
)

app_name = 'employee'

urlpatterns = [
    path('employees/', employee_list_view, name='employees'),
    path('employee/<int:id>/', employee_detail_view, name='employee_detail'),
    path('employee/add/', employee_add_view, name='employee_add'),
    path('employee/update/<int:id>/', employee_update_view, name='employee_update'),
    path('employee/delete/', employee_delete_view, name='employee_delete'),
]
