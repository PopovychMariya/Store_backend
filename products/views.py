from .models import Product
from .serializers import *
from rest_framework import viewsets, mixins, permissions, generics, filters
from accounts.permissions import IsSeller
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Product
from .serializers import ProductDetailsSerializer, ProductPreviewSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSeller]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_profile)
    
    def perform_update(self, serializer):
        if serializer.instance.seller != self.request.user.seller_profile:
            raise PermissionDenied("You do not have permission to edit this product.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.seller != self.request.user.seller_profile:
            raise PermissionDenied("You do not have permission to delete this product.")
        instance.delete()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductPreviewSerializer
        return ProductDetailsSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class CategoryListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryPreviewSerializer

class CategoryDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryPreviewSerializer
        return CategoryDetailSerializer
    
class SellerProductListView(generics.ListAPIView):
    serializer_class = SellerProductListSerializer

    def get_queryset(self):
        seller_id = self.kwargs.get('seller_id')
        return Product.objects.filter(seller__id=seller_id)