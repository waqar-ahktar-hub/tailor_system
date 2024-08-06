# # orders/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from notifications.models import Notification

# @receiver(post_save, sender=Order)
# def create_order_notification(sender, instance, created, **kwargs):
#     """Create a notification when an order is received or created."""
#     if created:
#         Notification.objects.create(
#             title="New Order Created",
#             message=f"An order with ID {instance.id} has been created for client {instance.client.name}.",
#             notification_type="alert"
#         )
#     else:
#         # For updates, you can add more specific conditions
#         Notification.objects.create(
#             title="Order Updated",
#             message=f"Order with ID {instance.id} has been updated.",
#             notification_type="alert"
#         )
# orders/signals.py
# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import Order
from notifications.models import Notification

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    """Create a notification when an order is received or created."""
    target_url = reverse('order:order_detail', args=[instance.id])
    
    if created:
        Notification.objects.create(
            title="New Order Created",
            message=f"An order with ID {instance.id} has been created for client {instance.client.name}.",
            notification_type="alert",
            target_url=target_url
        )
    else:
        Notification.objects.create(
            title="Order Updated",
            message=f"Order with ID {instance.id} has been updated.",
            notification_type="alert",
            target_url=target_url
        )

