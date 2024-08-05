"""Serializers class for TMS application."""

import re

from rest_framework import serializers


class LoginObjectSerializer(serializers.Serializer):
    """Serializer class for login api."""

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        """Custom-validations for login fields."""
        if self._validate_username(data['username']):
            return data
        else:
            raise serializers.ValidationError(
                "Username can not be empty & it can only have alphanumerics and underscores."
            )

        if self._validate_password(data['password']):
            return data
        else:
            raise serializers.ValidationError(
                "Password must be 8 character long or more."
            )

    def _validate_username(self, username):
        """Match valid username regex with username field."""
        return bool(re.match(
            r'[A-Za-z0-9_]{1,}',
            str(username)
        ))

    def _validate_password(self, password):
        """Match valid password regex with password field."""
        return bool(re.match(
            r'[\S]{8,}',
            str(password)
        ))
