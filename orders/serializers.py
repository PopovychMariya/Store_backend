from rest_framework import serializers
from .models import *

class CustomerOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ['product', 'product_name', 'date_of_purchase', 'quantity']

class SellerOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    customer_name = serializers.CharField(source='customer.user.username', read_only=True)
    class Meta:
        model = Order
        fields = ['product_name', 'date_of_purchase','quantity', 'customer_name']