"""All the Client APIs."""

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from client.models import Client
from client.serializer import ClientSerializer


class ClientView(APIView):
    """Class based view for Client for listing and adding."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get clients view."""
        clients = Client.objects.all()
        serializer_obj = ClientSerializer(clients, many=True)
        return JsonResponse(serializer_obj.data, safe=False, status=200)

    def post(self, request):
        """Add new client through post request."""
        data = JSONParser().parse(request)
        serializer_obj = ClientSerializer(data=data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return JsonResponse(serializer_obj.data, status=201)
        return JsonResponse(serializer_obj.errors, status=400)


client_view = ClientView.as_view()


class ClientDetailView(APIView):
    """Class based view for Client for updating, getting and deleting."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _get_object(self, pk):
        """First we see if client exists."""
        try:
            return Client.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """Get client by id view."""
        client = self._get_object(pk=pk)
        serializer_obj = ClientSerializer(client)
        return JsonResponse(serializer_obj.data, status=200)

    def put(self, request, pk, format=None):
        """Update client."""
        client = self._get_object(pk=pk)
        serializer_obj = ClientSerializer(client, data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return JsonResponse(serializer_obj.data, status=200)
        return JsonResponse(serializer_obj.errors, status=400)

    def delete(self, request, pk, format=None):
        """Delete existing client."""
        client = self._get_object(pk=pk)
        client.delete()
        return HttpResponse(status=204)


client_detail_view_api = ClientDetailView.as_view()
