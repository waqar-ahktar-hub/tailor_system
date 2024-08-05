"""Create dummy employees for testing purpose."""


from django.core.management.base import BaseCommand

from employee.models import Employee
from tms.constants import DUMMY_ADDRESS_MARKER
from tms.utils import RandomDataGenerator


class Command(BaseCommand, RandomDataGenerator):
    """Create dummy employees class."""

    help = "Create dummy employees for testing purposes."

    def add_arguments(self, parser):
        """Argument specifying how many dummy employees to create."""
        parser.add_argument(
            '--total', type=int, help='Indicates the number of employees to be created.', default=15,
        )

    def handle(self, *args, **kwargs):
        """Create 'total' dummy employees in database."""
        no_of_employees = kwargs['total']

        if no_of_employees < 1:
            self.stdout.write("Can not create -ive or zero number of employees.")

        else:
            name_set = self.get_n_unique_names(no_of_employees)

            existing_phones = Employee.objects.all().values_list('phone_number', flat=True)

            phone_set = self.get_n_unique_numbers(no_of_employees, existing_phones=existing_phones)
            employee_list = []

            for i in range(no_of_employees):
                employee = Employee(**{
                    'name': name_set[i],
                    'gender': 'M',
                    'phone_number': phone_set[i],
                    'address': DUMMY_ADDRESS_MARKER
                })
                employee_list.append(employee)

            Employee.objects.bulk_create(employee_list)
            self.stdout.write("Dummy employees created successfully.")
