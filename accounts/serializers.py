from rest_framework import serializers
from .models import BaseUser, CustomerUser, SellerUser

BASE_FIELDS = ('first_name', 'last_name', 'email', 'username', 'password')
CUSTOMER_FIELDS = ('user',)
SELLER_FIELDS = ('user', 'store_name', 'store_description',)

class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    user_type = serializers.SerializerMethodField()
    username = serializers.CharField(required=False)

    class Meta:
        model = BaseUser
        fields = BASE_FIELDS + ('user_type',)
    
    def get_user_type(self, obj):
        if obj.is_customer():
            return 'customer'
        elif obj.is_seller():
            return 'seller'
        return 'unknown'

    def validate_email(self, value):
        if self.instance:
            if BaseUser.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Email is already in use.")
        else:
            if BaseUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        if self.instance:
            if BaseUser.objects.filter(username=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Username is already in use.")
        else:
            if BaseUser.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username is already in use.")
        return value

    def create(self, validated_data):
        user = BaseUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        username = validated_data.pop('username', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        if username:
            instance.username = username

        instance.save()
        return instance

class UniversalRoleSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        fields = ('user',)

    def get_model_class(self):
        return self.Meta.model

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = BaseUser.objects.create_user(**user_data)
        return self.get_model_class().objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            base_user_serializer = BaseUserSerializer(instance=instance.user, data=user_data, partial=True)
            if base_user_serializer.is_valid():
                base_user_serializer.save()
            else:
                raise serializers.ValidationError(base_user_serializer.errors)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = BaseUserSerializer(instance.user).data
        representation['user'] = user_representation
        return representation

class CustomerUserSerializer(UniversalRoleSerializer):
    class Meta(UniversalRoleSerializer.Meta):
        model = CustomerUser
        fields = CUSTOMER_FIELDS

class SellerUserSerializer(UniversalRoleSerializer):
    class Meta(UniversalRoleSerializer.Meta):
        model = SellerUser
        fields = SELLER_FIELDS

class SellerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = ['store_name', 'store_description']
