from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = "__all__"
