"""Unit tests for Delete dummy clients command."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from client.models import Client
from tms.constants import DUMMY_EMAIL_MARKER
from tms.utils import TestDbSetUp


class DeleteDummyClientsTest(TestCase, TestDbSetUp):
    """Dummy clients deletion test class."""

    def setUp(self):
        """Setup client for deletion."""
        self.client = self.create_client(email_post_fix=DUMMY_EMAIL_MARKER)

    def test_delete_dummy_clients(self):
        """Test delete dummy clients command."""
        self.assertTrue(Client.objects.filter(email__endswith=DUMMY_EMAIL_MARKER).exists())
        console_output = StringIO()
        call_command('delete_dummy_clients', stdout=console_output)
        self.assertIn('Dummy clients deleted successfully.', console_output.getvalue())
        self.assertFalse(Client.objects.filter(email__endswith=DUMMY_EMAIL_MARKER))
