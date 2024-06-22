from rest_framework import serializers

from account.serializers import AddressSerializer
from product.models import Product

from .models import Order, OrderItem


# order-item serializer for serializing orderitems
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


# order serializer for serializing order
class OrderSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    order_items = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, obj):
        orderitems = obj.order_items.all()
        return OrderItemSerializer(instance=orderitems, many=True).data

    def get_address(self, obj):
        address = obj.address
        return AddressSerializer(instance=address).data


# product serializer for serializing products
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
