from rest_framework import serializers
from .models import OrderItem,Order
from product.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def create(self, validated_data):

        return OrderItem.objects.create(
            product=validated_data['product'],
            quantity=validated_data['quantity'],
        )

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'