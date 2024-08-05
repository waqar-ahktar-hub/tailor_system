"""Delete dummy employees for testing purpose."""

from django.core.management.base import BaseCommand

from employee.models import Employee
from tms.constants import DUMMY_ADDRESS_MARKER


class Command(BaseCommand):
    """Delete dummy employees command class."""

    help = "Delete dummy employees for clean database."

    def handle(self, *args, **kwargs):
        """Delete dummy employees from database."""
        Employee.objects.filter(address=DUMMY_ADDRESS_MARKER).delete()
        self.stdout.write('Dummy employees deleted successfully.')
