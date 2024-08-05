"""Modulus result of two numbers."""

from django import template

register = template.Library()


@register.filter
def get_modulus_value(num, val):
    """Return modulus of two numbers."""
    return num % val
