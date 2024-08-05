"""Context processors for TMS application."""

from django.urls import resolve


def template_title(request):
    """Add template title to template context."""
    url_name = resolve(request.path_info).url_name
    return {'title': url_name}
