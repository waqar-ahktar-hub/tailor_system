"""All the Client APIs."""

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tailor_management_system.serializers import LoginObjectSerializer


class LoginView(APIView):
    """Class based view loggin in user and returning Auth Token."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        """Check if user exists, return token if it does."""
        data = JSONParser().parse(request)
        serializer_obj = LoginObjectSerializer(data=data)
        if serializer_obj.is_valid():
            user = authenticate(username=serializer_obj.data['username'], password=serializer_obj.data['password'])
            if not user:
                return Response({'error': 'Invalid Credentials'}, status=404)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)

        return JsonResponse(serializer_obj.errors, status=400)


api_login_view = LoginView.as_view()
