"""Delete dummy orders for testing purpose."""

from django.core.management.base import BaseCommand

from order.models import Order
from tms.constants import DUMMY_ORDER_MARKER


class Command(BaseCommand):
    """Delete dummy orders command class."""

    help = "Delete dummy orders for clean database."

    def handle(self, *args, **kwargs):
        """Delete dummy orders from database."""
        Order.objects.filter(order=DUMMY_ORDER_MARKER).delete()
        self.stdout.write('Dummy orders deleted successfully.')
