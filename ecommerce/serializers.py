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


class AdminViewOrderListSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        response = super(AdminViewOrderListSerializer, self).to_representation(instance)
        order_details = OrderDetails.objects.filter(order_id=instance.id)
        response['order_details_info'] = OrderDetailSerializer(order_details, many=True).data
        order_price = OrderDetails.objects.filter(order_id=instance.id).aggregate(Sum('price'))
        print('price_sum ', order_price)
        response['total_order_amount'] = order_price['price__sum']
        return response
