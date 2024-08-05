"""Getting value from dictionary tag."""

from django import template

register = template.Library()


@register.simple_tag
def get_dict_value(dictionary, key):
    """Get value from dictionarty against a key."""
    return dictionary.get(key, 0)
