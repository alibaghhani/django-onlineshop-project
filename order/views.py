from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product
from .models import OrderItem
from .order import Order
from .serializers import OrderSerializer, OrderItemSerializer
from .forms import CartItemQuantityForm


# Create your views here.


class OrderItemView(APIView):
    def get(self,request ,format=None):
        order_item = OrderItem.objects.all()
        serilizer = OrderItemSerializer(order_item, many=True)
        return Response(serilizer.data)

    def post(self, request, format=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderView(View):
    def get(self,request):
        order = Order(request)
        return render(request,'order.html',{'order':order})

class AddItemToOrderView(View):
    def post(self,request,product_id):
        order = Order(request)
        product = get_object_or_404(Product,id=product_id)
        form = CartItemQuantityForm(request.POST)
        if form.is_valid():
            order.add(product, form.cleaned_data['quantity'])
        return redirect('order')
