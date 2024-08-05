"""Utility class for frequently needed functions."""

from django.core.exceptions import ObjectDoesNotExist

from client.models import FemaleMeasurements, MaleMeasurements


def get_measurements(client_id, client):
    """Get measurements against a client."""
    try:
        if client.gender == 'M':
            return MaleMeasurements.objects.get(client=client_id), True
        else:
            return FemaleMeasurements.objects.get(client=client_id), True
    except ObjectDoesNotExist:
        return None, False
