"""Serializers for models."""

import re

from rest_framework import serializers

from client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Client serializer for JSON-object & vice versa conversaiton."""

    class Meta:
        """Specified model for ModelSerializer."""

        model = Client
        fields = [
            'id',
            'name',
            'age',
            'gender',
            'address',
            'phone_number',
            'email'
        ]

    def validate(self, data):
        """Custom-validations for some of client fields."""
        if self._validate_name(data['name']):
            return data
        else:
            raise serializers.ValidationError(
                "Name can not have special characters, symbols or numbers"
            )

        if self._validate_phone_number(data['phone_number']):
            return data
        else:
            raise serializers.ValidationError(
                "Invalid phone number."
            )

    def _validate_name(self, name):
        """Match valid name regex with name field."""
        return bool(re.match(
            r'^[_A-z]*((-|\s)*[_A-z])*$',
            str(name)
        ))

    def _validate_phone_number(self, phone):
        """Match valid phone number regex with phone field."""
        return bool(re.match(
            r'^[+]{1,1}[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.0-9]{0,15}$',
            str(phone)
        ))
