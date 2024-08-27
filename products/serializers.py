from rest_framework import serializers
from .models import Product

class PreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price',]

class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'