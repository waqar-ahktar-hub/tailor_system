"""Forms for order application."""

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget

from order.models import Order, Task


class OrderForm(forms.ModelForm):
    """Order model mapped form."""

    order = forms.CharField(max_length=50, min_length=5)
    instructions = forms.CharField(widget=forms.Textarea, max_length=500, min_length=10)
    delivery_date = forms.DateField(widget=SelectDateWidget(empty_label="Delivery Date"))

    class Meta:
        """Specify fields to include."""

        model = Order
        exclude = ('date_recieved', 'client')

    def clean_delivery_date(self):
        """Check if date is valid."""
        delivery_date = self.cleaned_data['delivery_date']
        if delivery_date < datetime.date.today():
            raise ValidationError(('Delivery date can not be in past.'))

        return delivery_date

    def clean_status(self):
        """Check if status is valid."""
        status = self.cleaned_data['status']

        if (status == Order.DELIVERED) or (status == Order.CLOSED):
            incomplete_task_count = Task.objects.exclude(status=Task.COMPLETED).count()
            if incomplete_task_count:
                raise ValidationError(('Some tasks against this order are still pending, please finish them first.'))

        return status


class TaskForm(forms.ModelForm):
    """Task model mapped form."""

    description = forms.CharField(widget=forms.Textarea, max_length=500, min_length=10)
    deadline = forms.DateField(widget=SelectDateWidget(empty_label="Deadline"))

    class Meta:
        """Specify fields to include."""

        model = Task
        exclude = ('order',)

    def clean_deadline(self):
        """Check if date is valid."""
        deadline = self.cleaned_data['deadline']

        if deadline < datetime.date.today():
            raise ValidationError(('Deadline can not be in past.'))

        return deadline
