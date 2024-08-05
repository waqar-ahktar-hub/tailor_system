"""Tests for rest authentication.

This package includes all the unit tests for api based class authentication and crud operations.
"""

import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from client.models import Client
from tms.utils import TestDbSetUp


class WrapperTestClass:
    """Wrapper class for our TestCase class."""

    class ClientTestCase(TestCase, TestDbSetUp):
        """Common test case class having methods required in both basic and token auth tests."""

        def setUp(self):
            """Create a dummy user for the purpose of testing."""
            self.user, self.username, self.password = self.create_user()
            self.client = self.create_client()

        def test_get_login_response(self):
            """Test login."""
            api_client = self.get_authenticated_api_client()
            path = reverse('tailor_management_system:login_api')
            response = api_client.post(
                path=path,
                data=json.dumps({'username': self.username, 'password': self.password}),
                content_type='application/json'
            )
            token = json.loads(response.content)['token']
            token_from_db = Token.objects.get(user_id=self.user.id)
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(token)
            self.assertEqual(token, token_from_db.key)
            token_from_db.delete()

        def test_get_clients(self):
            """Test get client api."""
            api_client = self.get_authenticated_api_client()
            path = reverse('client:clients_api')
            response = api_client.get(
                path
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[0]['id'], self.client.id)

        def test_get_client_by_id(self):
            """Test get client details by id api."""
            api_client = self.get_authenticated_api_client()
            path = reverse('client:client_detail_api', kwargs={'pk': self.client.id})
            response = api_client.get(
                path
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)['email'], Client.objects.filter(id=1)[0].email)

        def test_update_client_by_id(self):
            """Test update client by id api."""
            api_client = self.get_authenticated_api_client()
            path = reverse('client:client_update_api', kwargs={'pk': self.client.id})
            data = {
                'name': 'Jon Snow',
                'age': 18,
                'gender': 'M',
                'address': 'night watch wall',
                'phone_number': '+9290078602',
                'email': self.client.email,
            }
            api_client.put(
                path=path,
                data=json.dumps(data),
                content_type='application/json'
            )
            self.assertTrue(Client.objects.filter(phone_number='+9290078602').exists())

        def test_add_client(self):
            """Add client by id api."""
            api_client = self.get_authenticated_api_client()
            path = reverse('client:client_add_api')
            data = {
                'name': 'Jon Snow',
                'age': 18,
                'gender': 'M',
                'address': 'night watch wall',
                'phone_number': '+9290078603',
                'email': 'jon.s@nightwatch.com',
            }
            api_client.post(
                path=path,
                data=json.dumps(data),
                content_type='application/json'
            )
            self.assertTrue(Client.objects.filter(email='jon.s@nightwatch.com').exists())

        def test_delete_client_by_id(self):
            """Delete client by id api."""
            api_client = self.get_authenticated_api_client()
            path = reverse('client:client_delete_api', kwargs={'pk': self.client.id})
            api_client.delete(
                path=path
            )
            self.assertFalse(Client.objects.filter(id=self.client.id).exists())
