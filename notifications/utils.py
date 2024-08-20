# notifications/utils.py

from django.contrib.auth.models import User
from django.utils import timezone
from .models import Notification  # Assuming you have a Notification model

def notify_admin_of_new_message(conversation):
    """Create a notification for the admin when a new message is sent."""
    for admin in User.objects.filter(is_superuser=True):
        Notification.objects.create(
            user=admin,
            message=f"New message in conversation with {conversation.client.username}",
            created_at=timezone.now()
        )
