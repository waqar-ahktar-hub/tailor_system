"""Forms for Client application."""

import re

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from client.models import Client, FemaleMeasurements, MaleMeasurements


# class ClientForm(forms.ModelForm):
#     """Client model mapped form."""

#     name = forms.CharField(max_length=50, min_length=4)
#     address = forms.CharField(widget=forms.Textarea, max_length=500, min_length=10)
#     phone_number = forms.CharField(max_length=15, min_length=6)

#     class Meta:
#         """Specify fields to include."""

#         model = Client
#         fields = '__all__'

#     def clean_name(self):
#         """Check if name is valid."""
#         name = self.cleaned_data['name']

#         if not self._validate_name(name):
#             raise ValidationError(('Invalid name.'))

#         return name

#     def clean_phone_number(self):
#         """Check if phone is valid."""
#         phone_number = self.cleaned_data['phone_number']

#         if not self._validate_phone_number(phone_number):
#             raise ValidationError(('Invalid phone number.'))

#         return phone_number

#     def _validate_name(self, name):
#         """Match valid name regex with name field."""
#         return bool(re.match(
#             r'^[_A-z]*((-|\s)*[_A-z])*$',
#             str(name)
#         ))

#     def _validate_phone_number(self, phone):
#         """Match valid phone number regex with phone field."""
#         return bool(re.match(
#             r'^[+]{1,1}[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.0-9]{0,15}$',
#             str(phone)
#         ))
# from django.contrib.auth.forms import UserCreationForm
# class ClientCreationForm(UserCreationForm):
#     class Meta:
#         model = Client
#         fields = ['username', 'email', 'phone_number', 'age', 'gender', 'address', 'password1', 'password2']



class ClientForm(forms.ModelForm):
    """Client model mapped form."""

    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Client
        fields = ['username', 'age', 'gender', 'address', 'phone_number', 'email', 'password']

    def clean_password(self):
        """Validate password field."""
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Password is required.')
        return password

    def save(self, commit=True):
        client = super().save(commit=False)
        if commit:
            user = User.objects.create_user(
                username=client.username,
                email=client.email,
                password=self.cleaned_data['password']
            )
            client.user = user
            client.save()
        return client



class MaleMeasurementsForm(forms.ModelForm):
    """MaleMeasurements model mapped form."""

    class Meta:
        """Specify fields to include."""

        model = MaleMeasurements
        exclude = ('client',)


class FemaleMeasurementsForm(forms.ModelForm):
    """FemaleMeasurements model mapped form."""

    class Meta:
        """Specify fields to include."""

        model = FemaleMeasurements
        exclude = ('client',)
