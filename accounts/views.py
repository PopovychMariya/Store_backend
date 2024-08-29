from rest_framework import generics, permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from .models import *
from .serializers import *
from products.models import Product
from products.serializers import SellerProductListSerializer


class ProfileCreateViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def create(self, request):
        user_type = request.data.get('user_type')
        if user_type == 'customer':
            serializer = CustomerUserSerializer(data=request.data)
        elif user_type == 'seller':
            serializer = SellerUserSerializer(data=request.data)
        else:
            raise ValidationError({"error": "Invalid user type"})
        
        user_data = request.data.get('user', {})
        username = user_data.get('username')
        password = user_data.get('password')

        if not username:
            raise ValidationError({"username": "This field is required."})
        if not password:
            raise ValidationError({"password": "This field is required."})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'seller_profile'):
            profile = user.seller_profile
            user_type = "seller"
        elif hasattr(user, 'customer_profile'):
            profile = user.customer_profile
            user_type = "customer"
        else:
            raise ValueError("No associated profile found for this user.")
        
        self.role = user_type
        return profile

    def get_serializer_class(self):
        if hasattr(self.request.user, 'customer_profile'):
            return CustomerUserSerializer
        elif hasattr(self.request.user, 'seller_profile'):
            return SellerUserSerializer
        return BaseUserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        data = serializer.data
        data['user_type'] = self.role
        return Response(data)

    def update(self, request, *args, **kwargs):
        user = request.user
        user_data = request.data.get('user', {})

        base_user_serializer = BaseUserSerializer(instance=user, data=user_data, partial=True)
        if base_user_serializer.is_valid():
            base_user_serializer.save()
        else:
            return Response(base_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        profile_data = request.data.copy()
        profile_data.pop('user', None)

        serializer_class = self.get_serializer_class()
        profile = self.get_object()
        serializer = serializer_class(instance=profile, data=profile_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.delete() if hasattr(instance, 'user') else instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    
class SellerShopView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_seller():
            seller_profile = user.seller_profile
            products = Product.objects.filter(seller=seller_profile)
            serializer = SellerProductListSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "User is not a seller."}, status=400)
