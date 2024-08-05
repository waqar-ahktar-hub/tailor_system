"""Get product from key."""

from django import template

from product.models import Product

register = template.Library()


@register.simple_tag
def get_product_from_key(key):
    """Return product against an id."""
    return Product.objects.filter(id=key).first()
