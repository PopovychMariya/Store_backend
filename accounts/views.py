from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from .serializers import *


def metadata_instance(field_name, field):
    return {
        "name": field_name,
        "label": field.label if field.label else field_name.capitalize(),
        "type": "password" if "password" in field_name else "text",
        "required": field.required,
    }

class RegistrationMetadataView(APIView):
    def get(self, request, user_type=None):
        if user_type == 'customer':
            serializer = CustomerUserSerializer()
        elif user_type == 'seller':
            serializer = SellerUserSerializer()
        else:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
        
        metadata = []
        for field_name, field in serializer.fields.items():
            if field_name == 'user':
                user_metadata = {
                    "name": "user",
                    "label": "User Information",
                    "type": "nested",
                    "required": True,
                    "fields": [
                        metadata_instance(user_field_name, user_field)
                        for user_field_name, user_field in BaseUserSerializer().fields.items()
                    ]
                }
                metadata.append(user_metadata)
            else:
                metadata.append(metadata_instance(field_name, field))
        return Response({"fields": metadata})


class RegistrationView(generics.CreateAPIView):
    def get_serializer_class(self):
        user_type = self.request.data.get('user_type')
        if user_type == 'customer':
            return CustomerUserSerializer
        elif user_type == 'seller':
            return SellerUserSerializer
        raise ValidationError({"error": "Invalid user type"})
    

class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if hasattr(user, 'customer_profile'):
            return user.customer_profile
        elif hasattr(user, 'seller_profile'):
            return user.seller_profile
        else:
            return user

    def get_serializer_class(self):
        user = self.request.user

        if hasattr(user, 'customer_profile'):
            return CustomerUserSerializer
        elif hasattr(user, 'seller_profile'):
            return SellerUserSerializer
        else:
            return BaseUserSerializer
        
class ProfileDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if hasattr(user, 'customer_profile'):
            return user.customer_profile
        elif hasattr(user, 'seller_profile'):
            return user.seller_profile
        else:
            return user

    def perform_destroy(self, instance):
        if isinstance(instance, get_user_model()):
            instance.delete()
        else:
            instance.delete()
            user = self.request.user
            user.delete()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)