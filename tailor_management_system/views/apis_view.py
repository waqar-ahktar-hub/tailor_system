# api_views.py

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tailor_management_system.serializers import LoginObjectSerializer
from rest_framework import status
from client.models import Client


class LoginView(APIView):
    """Class-based view for client login and returning Auth Token."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate client and return token and dashboard URL."""
        data = JSONParser().parse(request)
        serializer_obj = LoginObjectSerializer(data=data)
        if serializer_obj.is_valid():
            user = authenticate(email=serializer_obj.data['username'], password=serializer_obj.data['password'])
            if not user:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
            
            token, _ = Token.objects.get_or_create(user=user)
            if user.is_superuser:
                dashboard_url = '/admin_dashboard/'  # Admin dashboard URL
            else:
                dashboard_url = '/client_dashboard/'  # Client dashboard URL

            return Response({'token': token.key, 'dashboard_url': dashboard_url}, status=status.HTTP_200_OK)

        return JsonResponse(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

api_login_view = LoginView.as_view()

class LogoutView(APIView):
    """Class-based view to log out a client by deleting their Auth Token."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete the client's token to log them out."""
        try:
            request.user.auth_token.delete()
            return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response({"error": "Invalid token or token not provided."}, status=status.HTTP_400_BAD_REQUEST)









# """All the Client APIs."""

# from django.contrib.auth import authenticate
# from django.http import JsonResponse
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token
# from rest_framework.parsers import JSONParser
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from tailor_management_system.serializers import LoginObjectSerializer
# from rest_framework import status

# class LoginView(APIView):
#     """Class based view loggin in user and returning Auth Token."""

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]

#     def post(self, request):
#         """Check if user exists, return token if it does."""
#         data = JSONParser().parse(request)
#         serializer_obj = LoginObjectSerializer(data=data)
#         if serializer_obj.is_valid():
#             user = authenticate(username=serializer_obj.data['username'], password=serializer_obj.data['password'])
#             if not user:
#                 return Response({'error': 'Invalid Credentials'}, status=404)
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=200)

#         return JsonResponse(serializer_obj.errors, status=400)


# api_login_view = LoginView.as_view()

# class LogoutView(APIView):
#     """Class-based view to log out a user by deleting their Auth Token."""

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         """Delete the user's token to log them out."""
#         try:
#             request.user.auth_token.delete()
#             return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except (AttributeError, Token.DoesNotExist):
#             return Response({"error": "Invalid token or token not provided."}, status=status.HTTP_400_BAD_REQUEST)
