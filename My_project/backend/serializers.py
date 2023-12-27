from rest_framework import serializers
from backend.models import (
    User,
    Category,
    Shop,
    ProductInfo,
    Product,
    ProductParameter,
    OrderItem,
    Order,
    Contact,
)


class ContactSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    pass


class ShopSerializer(serializers.ModelSerializer):
    pass


class ProductSerializer(serializers.ModelSerializer):
    pass


class ProductParameterSerializer(serializers.ModelSerializer):
    pass


class ProductInfoSerializer(serializers.ModelSerializer):
    pass


class OrderItemSerializer(serializers.ModelSerializer):
    pass


class OrderItemCreateSerializer(serializers.Model):
    pass


class OrderSerializer(serializers.ModelSerializer):
    pass
