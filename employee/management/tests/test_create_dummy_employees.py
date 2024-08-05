"""Unit tests for create dummy employees command."""

from io import StringIO

import ddt
from django.core.management import call_command
from django.test import TestCase

from tms.utils import TestDbSetUp


@ddt.ddt
class CreateDummyClientsTest(TestCase, TestDbSetUp):
    """Dummy employees creation test class."""

    @ddt.data(
        (0, 'Can not create -ive or zero number of employees.'),
        (-1, 'Can not create -ive or zero number of employees.'),
        (100, 'Dummy employees created successfully.')
    )
    @ddt.unpack
    def test_create_dummy_employees(self, total, msg):
        """Test create dummy employees command."""
        out = StringIO()
        call_command('create_dummy_employees', '--total={}'.format(total), stdout=out)
        self.assertIn(msg, out.getvalue())
