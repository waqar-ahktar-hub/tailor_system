"""Create dummy employees for testing purpose."""

from django.core.management.base import BaseCommand

from client.models import Client
from order.models import Order
from tms.constants import DUMMY_EMAIL_MARKER, DUMMY_ORDER_MARKER
from tms.utils import RandomDataGenerator, get_future_date


class Command(BaseCommand, RandomDataGenerator):
    """Create dummy orders class."""

    help = "Create dummy orders for testing purposes."

    def add_arguments(self, parser):
        """Argument specifying how many dummy employees to create."""
        parser.add_argument(
            '--total', type=int, help='Indicates the number of clients to be created.', default=5,
        )

    def handle(self, *args, **kwargs):
        """Create 'total' dummy orders in database."""
        no_of_orders = kwargs['total']
        clients = Client.objects.filter(email__endswith=DUMMY_EMAIL_MARKER)

        if (no_of_orders < 1) or (clients.count() == 0):
            self.stdout.write("Can not create -ive or zero number of orders against zero clients.")

        else:
            no_of_chosen_clients = self.get_random_number(lower_limit=1, upper_limit=clients.count())

            orders = []
            for client in clients:
                for i in range(0, no_of_orders):
                    order = Order(
                        **{
                            'client': client,
                            'status': Order.RECIEVED,
                            'payment_status': False,
                            'payment_amount': 10000,
                            'advance_payment_amount': 2000,
                            'order': DUMMY_ORDER_MARKER,
                            'instructions': DUMMY_ORDER_MARKER,
                            'delivery_date': get_future_date(5)
                        }
                    )
                    orders.append(order)

            Order.objects.bulk_create(orders)
            self.stdout.write("Dummy orders created successfully.")
