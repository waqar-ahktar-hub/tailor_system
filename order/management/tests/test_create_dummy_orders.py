"""Unit tests for create dummy orders command."""

from io import StringIO

import ddt
from django.core.management import call_command
from django.test import TestCase

from tms.constants import DUMMY_EMAIL_MARKER
from tms.utils import TestDbSetUp


@ddt.ddt
class CreateDummyClientsTest(TestCase, TestDbSetUp):
    """Dummy orders creation test class."""

    def setUp(self):
        """Create a dummy user for the purpose of testing."""
        self.user, self.username, self.password = self.create_user()
        self.client = self.create_client(email_post_fix=DUMMY_EMAIL_MARKER)

    @ddt.data(
        (0, 'Can not create -ive or zero number of orders against zero clients.'),
        (-1, 'Can not create -ive or zero number of orders against zero clients.'),
        (100, 'Dummy orders created successfully.')
    )
    @ddt.unpack
    def test_create_dummy_orders(self, total, msg):
        """Test create dummy orders command."""
        console_output = StringIO()
        call_command('create_dummy_orders', '--total={}'.format(total), stdout=console_output)
        self.assertIn(msg, console_output.getvalue())
