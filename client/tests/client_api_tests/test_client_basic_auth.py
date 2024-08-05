"""Basic authentication based test cases."""

from rest_framework.test import APIClient

from client.tests.client_api_tests import WrapperTestClass


class BasicAuthTests(WrapperTestClass.ClientTestCase):
    """Basic auth based client tests."""

    def get_authenticated_api_client(self):
        """Forced auth api client."""
        api_client = APIClient()
        api_client.force_authenticate(user=self.user)
        return api_client
