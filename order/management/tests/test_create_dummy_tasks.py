"""Unit tests for create dummy tasks command."""

from io import StringIO

import ddt
from django.core.management import call_command
from django.test import TestCase

from tms.constants import DUMMY_EMAIL_MARKER
from tms.utils import TestDbSetUp


@ddt.ddt
class CreateDummyTasksTest(TestCase, TestDbSetUp):
    """Dummy tasks creation test class."""

    def setUp(self):
        """Create a dummy user for the purpose of testing."""
        self.user, self.username, self.password = self.create_user()
        self.client = self.create_client(email_post_fix=DUMMY_EMAIL_MARKER)
        self.order = self.create_order(self.client)
        self.employee = self.create_employee()

    @ddt.data(
        (0, 'Can not create -ive or zero number of tasks against 0 or no orders.'),
        (-1, 'Can not create -ive or zero number of tasks against 0 or no orders.'),
        (100, 'Dummy tasks created successfully.')
    )
    @ddt.unpack
    def test_create_dummy_tasks(self, total, msg):
        """Test create dummy tasks command."""
        console_output = StringIO()
        call_command('create_dummy_tasks', '--total={}'.format(total), stdout=console_output)
        self.assertIn(msg, console_output.getvalue())
