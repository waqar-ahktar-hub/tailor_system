"""Client applciation configuratoin."""

from django.apps import AppConfig


class ClientConfig(AppConfig):
    """Config class for client application."""

    name = 'client'
    # def ready(self):
    #     import client.signals  # noqa