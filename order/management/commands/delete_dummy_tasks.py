"""Delete dummy tasks for testing purpose."""

from django.core.management.base import BaseCommand

from order.models import Task
from tms.constants import DUMMY_TASK_MARKER


class Command(BaseCommand):
    """Delete dummy tasks command class."""

    help = "Delete dummy tasks for clean database."

    def handle(self, *args, **kwargs):
        """Delete dummy tasks from database."""
        Task.objects.filter(description=DUMMY_TASK_MARKER).delete()
        self.stdout.write('Dummy tasks deleted successfully.')
