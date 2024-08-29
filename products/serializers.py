from rest_framework import serializers
from .models import Category, Product
from accounts.serializers import SellerDetailSerializer

class ProductPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price',]

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'in_stock']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['seller_id'] = instance.seller.id
        return representation

class CategoryPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductPreviewSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Category
        fields = ['id', 'name', 'products',]

class SellerProductListSerializer(serializers.Serializer):
    seller = SellerDetailSerializer(source='seller')
    products = serializers.SerializerMethodField()

    def get_products(self, instance):
        if isinstance(instance, list) or hasattr(instance, '__iter__'):
            return ProductPreviewSerializer(instance, many=True).data
        else:
            return ProductPreviewSerializer([instance], many=True).data

    def to_representation(self, instance):
        
        if hasattr(instance, '__iter__') and not isinstance(instance, str):
            seller_instance = instance.first().seller if instance else None
        else:
            seller_instance = instance.seller

        return {
            'store_name': seller_instance.store_name if seller_instance else '',
            'store_description': seller_instance.store_description if seller_instance else '',
            'products': self.get_products(instance)
        }
    