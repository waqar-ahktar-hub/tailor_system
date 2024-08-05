"""Tests for product application."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from tms.utils import TestDbSetUp


class ProductImagesTestCases(TestCase, TestDbSetUp):
    """Unit tests for product operations."""

    def setUp(self):
        """Set up client, user and order for tests."""
        self.api_client = APIClient()
        self.user, self.username, self.password = self.create_user()
        self.product = self.create_product()
        self.product_images = self.create_product_images(self.product)

    def get_add_product_images(self):
        """Add product images test case."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('product:product_images_add', kwargs={'product_id': self.product.id})
        response = self.api_client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_images/add-product_images.html')
