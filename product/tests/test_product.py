"""Tests for product application."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from product.forms import ProductForm
from product.models import Product
from tms.utils import TestDbSetUp


class ProductTestCases(TestCase, TestDbSetUp):
    """Unit tests for product operations."""

    def setUp(self):
        """Set up client, user and order for tests."""
        self.api_client = APIClient()
        self.user, self.username, self.password = self.create_user()
        self.product = self.create_product()

    def test_list_products(self):
        """Get products test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('product:products')
        response = self.api_client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/list-products.html')

    def test_detail_product(self):
        """Get product test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('product:product_detail', kwargs={'id': self.product.id})
        response = self.api_client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product-detail.html')

    def test_add_product(self):
        """Check add product template."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('product:product_add')
        response = self.api_client.get(
            path
        )
        form = response.context['form']
        self.assertTemplateUsed(response, 'product/add-product.html')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, ProductForm)

    def test_delete_product(self):
        """Delete product test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('product:product_delete')
        data = {'id': self.product.id}
        response = self.api_client.post(path=path, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
