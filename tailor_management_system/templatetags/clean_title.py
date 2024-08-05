"""Title cleaning custom tag."""

from django import template

register = template.Library()


@register.simple_tag
def clean_title(title):
    """Convert string to title case."""
    return title.replace('_', ' ').title()
