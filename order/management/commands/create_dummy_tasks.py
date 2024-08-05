"""Create dummy employees for testing purpose."""

from django.core.management.base import BaseCommand

from employee.models import Employee
from order.models import Order, Task
from tms.constants import DUMMY_ADDRESS_MARKER, DUMMY_ORDER_MARKER, DUMMY_TASK_MARKER
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
        """Create 'total' dummy tasks in database."""
        no_of_tasks = kwargs['total']
        orders = Order.objects.filter(order=DUMMY_ORDER_MARKER)

        if (no_of_tasks < 1) or (orders.count() == 0):
            self.stdout.write("Can not create -ive or zero number of tasks against 0 or no orders.")

        else:
            no_of_orders = self.get_random_number(lower_limit=1, upper_limit=no_of_tasks)
            dummy_employees = Employee.objects.filter(address=DUMMY_ADDRESS_MARKER)
            dummy_employees_count = dummy_employees.count()

            tasks = []
            for order in orders:
                for i in range(0, no_of_tasks):
                    task = Task(
                        **{
                            'order': order,
                            'status': Task.TASK_STATUS_CHOICES[self.get_random_number(lower_limit=0, upper_limit=3)][0],
                            'description': DUMMY_TASK_MARKER,
                            'deadline': get_future_date(5),
                            'employee': dummy_employees[self.get_random_number(upper_limit=dummy_employees_count)]
                        }
                    )
                    tasks.append(task)

            Task.objects.bulk_create(tasks)
            self.stdout.write("Dummy tasks created successfully.")
