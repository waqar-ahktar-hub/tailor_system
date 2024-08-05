"""Unit tests for Delete dummy employees command."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from employee.models import Employee
from tms.constants import DUMMY_ADDRESS_MARKER
from tms.utils import TestDbSetUp


class DeleteDummyEmployeesTest(TestCase, TestDbSetUp):
    """Dummy employees deletion test class."""

    def setUp(self):
        """Setup employee for deletion."""
        self.employee = self.create_employee()

    def test_delete_dummy_employees(self):
        """Test delete dummy employees command."""
        self.assertTrue(Employee.objects.filter(address=DUMMY_ADDRESS_MARKER).exists())
        console_output = StringIO()
        call_command('delete_dummy_employees', stdout=console_output)
        self.assertIn('Dummy employees deleted successfully.', console_output.getvalue())
        self.assertFalse(Employee.objects.filter(address=DUMMY_ADDRESS_MARKER))
