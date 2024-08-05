"""Unit tests for client application's CRUD opeartions."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from client.forms import ClientForm, MaleMeasurementsForm
from client.models import Client
from tms.utils import TestDbSetUp


class ClientTestCase(TestCase, TestDbSetUp):
    """Unit test for Client model's CRUD functionality."""

    api_client = APIClient()

    def setUp(self):
        """Create a dummy user for the purpose of testing."""
        self.api_client = APIClient()
        self.user, self.username, self.password = self.create_user()
        self.client = self.create_client()
        self.measurements = self.create_male_measurements(self.client)

    def test_login(self):
        """Login test case."""
        path = reverse('login')
        response = self.api_client.post(path, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)

    def test_list_clients(self):
        """ Check list of clients."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('client:clients')
        response = self.api_client.get(
            path
        )
        self.assertTemplateUsed(response, 'client/list-clients.html')
        self.assertEqual(response.status_code, 200)
        self.api_client.logout()

    def test_add_client(self):
        """Check add client template."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('client:client_add')
        response = self.api_client.get(
            path
        )
        form = response.context['form']
        self.assertTemplateUsed(response, 'client/add-client.html')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, ClientForm)
        self.api_client.logout()

    def test_details_client(self):
        """Detail of client and measurements."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('client:client_detail', kwargs={'pk': self.client.id})
        response = self.api_client.get(
            path
        )
        self.assertTemplateUsed(response, 'client/client-detail.html')
        self.assertEqual(response.status_code, 200)
        self.api_client.logout()

    def test_add_measurement(self):
        """Get add view of measurement."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('client:measurment_add', kwargs={'client_id': self.client.id})
        response = self.api_client.get(
            path
        )
        form = response.context['form']
        self.assertTemplateUsed(response, 'client/add-measurements.html')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form(), MaleMeasurementsForm)
        self.api_client.logout()

    def test_delete_clients(self):
        """Delete client."""
        self.api_client.login(username=self.username, password=self.password)
        path = reverse('client:client_delete')
        data = {'id': self.client.id}
        response = self.api_client.post(path, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.count(), 0)
        self.api_client.logout()
