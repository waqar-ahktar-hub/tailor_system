"""Forms for order application."""

import re

from django import forms
from django.core.exceptions import ValidationError

from product.models import Product, ProductImages


class ProductForm(forms.ModelForm):
    """Product model mapped form."""

    title = forms.CharField(max_length=30, min_length=4)
    product_type = forms.CharField(max_length=30, min_length=4)
    description = forms.CharField(widget=forms.Textarea, min_length=10)

    class Meta:
        """Specify fields to include."""

        model = Product
        fields = '__all__'

    def clean_title(self):
        """Check if title is valid."""
        title = self.cleaned_data['title']

        if not self._validate_text(title):
            raise ValidationError(('Invalid title.'))

        return title

    def clean_product_type(self):
        """Check if type is valid."""
        product_type = self.cleaned_data['product_type']

        if not self._validate_text(product_type):
            raise ValidationError(('Invalid product_type.'))

        return product_type

    def _validate_text(self, text):
        """Match valid text regex with text field."""
        return bool(re.match(
            r'^[_A-z0-9]*((-|\s)*[_A-z0-9])*$',
            str(text)
        ))


class ProductImagesForm(forms.ModelForm):
    """Product image model mapped form."""

    class Meta:
        """Meta for PI."""

        model = ProductImages
        exclude = ('product',)
