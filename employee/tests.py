"""Tests for employee application."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from employee.forms import EmployeeForm
from employee.models import Employee
from tms.utils import TestDbSetUp


class EmployeeTestCases(TestCase, TestDbSetUp):
    """Unit tests for order operations."""

    def setUp(self):
        """Set up client, user and order for tests."""
        self.api_client = APIClient()
        self.user, self.username, self.password = self.create_user()
        self.employee = self.create_employee()

    def test_list_employees(self):
        """Get employees test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('employee:employees')
        response = self.api_client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/list-employees.html')

    def test_detail_employee(self):
        """Get employees test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('employee:employee_detail', kwargs={'id': self.employee.id})
        response = self.api_client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/employee-detail.html')

    def test_add_employee(self):
        """Check add employee template."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('employee:employee_add')
        response = self.api_client.get(
            path
        )
        form = response.context['form']
        self.assertTemplateUsed(response, 'employee/add-employee.html')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, EmployeeForm)

    def test_delete_employee(self):
        """Delete employee test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('employee:employee_delete')
        data = {'id': self.employee.id}
        response = self.api_client.post(path, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())
