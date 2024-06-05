from rest_framework import serializers
from account.serializers import AddressSerializer
from .models import OrderItem,Order
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


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

    def get_address(self,obj):
        address_ = obj.address.all()
        return AddressSerializer(instance=address_,many=True).data




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'