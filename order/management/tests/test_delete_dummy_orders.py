"""Unit tests for Delete dummy orders command."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from order.models import Order
from tms.constants import DUMMY_EMAIL_MARKER, DUMMY_ORDER_MARKER
from tms.utils import TestDbSetUp


class DeleteDummyOrdersTest(TestCase, TestDbSetUp):
    """Dummy orders deletion test class."""

    def setUp(self):
        """Setup order for deletion."""
        self.client = self.create_client(email_post_fix=DUMMY_EMAIL_MARKER)
        self.order = self.create_order(self.client)

    def test_delete_dummy_orders(self):
        """Test delete dummy orders command."""
        console_output = StringIO()
        self.assertTrue(Order.objects.filter(order=DUMMY_ORDER_MARKER).exists())
        call_command('delete_dummy_orders', stdout=console_output)
        self.assertIn('Dummy orders deleted successfully.', console_output.getvalue())
        self.assertFalse(Order.objects.filter(order=DUMMY_ORDER_MARKER).exists())
