"""Tests for order application."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from order.forms import OrderForm
from tms.utils import TestDbSetUp


class OrderTestCase(TestCase, TestDbSetUp):
    """Unit tests for order operations."""

    def setUp(self):
        """Set up client, user and order for tests."""
        self.api_client = APIClient()
        self.user, self.username, self.password = self.create_user()
        self.client = self.create_client()
        self.order = self.create_order(self.client)

    def test_get_orders(self):
        """Get order test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('order:orders')
        response = self.api_client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/list-orders.html')

    def test_get_order(self):
        """Get order test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('order:order_detail', kwargs={'id': self.order.id})
        response = self.api_client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order-detail.html')

    def test_add_order(self):
        """Check add order template."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('order:order_add', kwargs={'client_id': self.client.id})
        response = self.api_client.get(
            path
        )
        form = response.context['form']
        self.assertTemplateUsed(response, 'order/add-order.html')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, OrderForm)
