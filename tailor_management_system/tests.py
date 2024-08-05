"""Tests for tailor management system application."""


from django.template import Context, Template
from django.test import TestCase


class TMSTestCases(TestCase):
    """Unit tests for TMS Application."""

    def test_get_title_custom_tag(self):
        """The custom tag for title creation."""
        out = Template(
            "{% load clean_title %}"
            "{% clean_title title %}"
        ).render(Context({'title': 'dashboard'}))
        self.assertEqual(out, "Dashboard")
