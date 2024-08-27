BASE_FIELDS = ('first_name', 'last_name', 'email', 'username', 'password')
CUSTOMER_FIELDS = ('user',)
SELLER_FIELDS = ('user', 'store_name', 'store_description',)

from rest_framework import serializers
from .models import BaseUser , CustomerUser, SellerUser

class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = BASE_FIELDS

    def validate_email(self, value):
        if BaseUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        if BaseUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value

    def create(self, validated_data):
        return BaseUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class CustomerUserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta(BaseUserSerializer.Meta):
        model = CustomerUser
        fields = CUSTOMER_FIELDS

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = BaseUser.objects.create_user(**user_data)
        return CustomerUser.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            super().update(instance.user, user_data)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = BaseUserSerializer(instance.user).data
        representation['user'] = user_representation
        return representation


class SellerUserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta(BaseUserSerializer.Meta):
        model = SellerUser
        fields = SELLER_FIELDS

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = BaseUser.objects.create_user(**user_data)
        return SellerUser.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            super().update(instance.user, user_data)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = BaseUserSerializer(instance.user).data
        representation['user'] = user_representation
        return representation