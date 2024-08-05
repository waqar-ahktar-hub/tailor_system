"""Get which group a page belongs to."""

from django import template

register = template.Library()


@register.simple_tag
def get_page_group(title, *args, **kwargs):
    """Get page group from title."""
    DASHBOARD_GROUP = 'DASHBOARD'
    CLIENT_GROUP = 'CLIENT'
    PRODUCT_GROUP = 'PRODUCT'
    EMPLOYEE_GROUP = 'EMPLOYEE'
    ORDER_GROUP = 'ORDER'
    TASK_GROUP = 'TASK'

    if ('client' in title) or ('measurment' in title):
        return CLIENT_GROUP
    elif 'product' in title:
        return PRODUCT_GROUP
    elif 'dashboard' in title:
        return DASHBOARD_GROUP
    elif 'employee' in title:
        return EMPLOYEE_GROUP
    elif 'order' in title:
        return ORDER_GROUP
    elif 'task' in title:
        return TASK_GROUP
    else:
        return 'None'
