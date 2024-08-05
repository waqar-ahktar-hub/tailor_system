"""Views for measurements."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import View

from client.forms import FemaleMeasurementsForm, MaleMeasurementsForm
from client.models import Client, FemaleMeasurements, MaleMeasurements


class MeasurementsAddView(LoginRequiredMixin, View):
    """Class based view for adding MaleMeasurements."""

    def _add_measurements(self, request, Form, client):
        """Add measurement's return function to avoid duplication."""
        form = Form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            return redirect('client:client_detail', pk=client.id)
        else:
            return render(request, 'client/add-measurements.html', {'form': form, 'func': 'Add'})

    def _get_add_measurements(self, request, form, client):
        """Add measurement's get function to avoid duplication."""
        return render(
            request,
            'client/add-measurements.html',
            {'form': form, 'client': client, 'func': 'Add'}
        )

    def get(self, request, client_id):
        """Return add new client form."""
        client = get_object_or_404(Client, id=client_id)
        if client.gender == 'M':
            return self._get_add_measurements(request, MaleMeasurementsForm, client)
        else:
            return self._get_add_measurements(request, FemaleMeasurementsForm, client)

    def post(self, request, client_id):
        """Save male measurements and redirect to index."""
        client = get_object_or_404(Client, id=client_id)
        if client.gender == 'M':
            return self._add_measurements(request, MaleMeasurementsForm, client)
        else:
            return self._add_measurements(request, FemaleMeasurementsForm, client)


measurements_add_view = MeasurementsAddView.as_view()


class MeasurementsUpdateView(LoginRequiredMixin, View):
    """Class based view for adding MaleMeasurements."""

    def _update_measurements(self, request, Form, client, instance):
        """Update measurement's function to avoid duplication."""
        form = Form(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            return redirect('client:client_detail', pk=client.id)
        else:
            return render(request, 'client/add-measurements.html', {'form': form})

    def _get_update_measurements(self, request, Form, client, instance):
        """Update measurement's get function to avoid duplication."""
        form = Form(instance=instance)
        return render(
            request,
            'client/add-measurements.html',
            {'form': form, 'client': client, 'func': 'Update'}
        )

    def get(self, request, client_id):
        """Return add new client form."""
        client = get_object_or_404(Client, id=client_id)
        if client.gender == 'M':
            instance = get_object_or_404(MaleMeasurements, client=client)
            return self._get_update_measurements(request, MaleMeasurementsForm, client, instance)
        else:
            instance = get_object_or_404(FemaleMeasurements, client=client)
            return self._get_update_measurements(request, FemaleMeasurementsForm, client, instance)

    def post(self, request, client_id):
        """Save male measurements and redirect to index."""
        client = get_object_or_404(Client, id=client_id)
        if client.gender == 'M':
            measurements = get_object_or_404(MaleMeasurements, client=client)
            return self._update_measurements(request, MaleMeasurementsForm, client, measurements)
        else:
            measurements = get_object_or_404(FemaleMeasurements, client=client)
            return self._update_measurements(request, FemaleMeasurementsForm, client, measurements)


measurements_update_view = MeasurementsUpdateView.as_view()
