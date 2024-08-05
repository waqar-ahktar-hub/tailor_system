"""Unit tests for Delete dummy tasks command."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from order.models import Task
from tms.constants import DUMMY_EMAIL_MARKER, DUMMY_ORDER_MARKER, DUMMY_TASK_MARKER
from tms.utils import TestDbSetUp


class DeleteDummyTasksTest(TestCase, TestDbSetUp):
    """Dummy tasks deletion test class."""

    def setUp(self):
        """Setup order for deletion."""
        self.client = self.create_client(email_post_fix=DUMMY_EMAIL_MARKER)
        self.order = self.create_order(self.client)
        self.employee = self.create_employee()
        self.task = self.create_task(self.order, self.employee)

    def test_delete_dummy_tasks(self):
        """Test delete dummy tasks command."""
        self.assertTrue(Task.objects.filter(description=DUMMY_TASK_MARKER).exists())
        console_output = StringIO()
        call_command('delete_dummy_tasks', stdout=console_output)
        self.assertIn('Dummy tasks deleted successfully.', console_output.getvalue())
        self.assertFalse(Task.objects.filter(description=DUMMY_ORDER_MARKER).exists())
