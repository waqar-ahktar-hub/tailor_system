"""Delete dummy clients for testing purpose."""

from django.core.management.base import BaseCommand

from client.models import Client
from tms.constants import DUMMY_EMAIL_MARKER


class Command(BaseCommand):
    """Delete dummy clients command class."""

    help = "Delete dummy clients for clean database."

    def handle(self, *args, **kwargs):
        """Delete dummy clients from database."""
        Client.objects.filter(email__endswith=DUMMY_EMAIL_MARKER).delete()
        self.stdout.write('Dummy clients deleted successfully.')
