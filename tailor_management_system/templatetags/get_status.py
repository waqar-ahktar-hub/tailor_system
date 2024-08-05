"""Get proper status word against key."""

from django import template

from order.models import Order, Task

register = template.Library()


@register.simple_tag
def get_status(module, status_key):
    """Match module and status key to return proper status."""
    order_status_dict = dict(Order.ORDER_STATUS_CHOICES)
    task_status_dict = dict(Task.TASK_STATUS_CHOICES)

    if module == 'ORDER':
        return order_status_dict[status_key]
    else:
        return task_status_dict[status_key]
