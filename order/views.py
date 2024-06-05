from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Address
from config.settings import ORDER_MODEL
from product.models import Product
from .models import OrderItem, Order
from .cart import Cart
from .serializers import OrderSerializer, OrderItemSerializer
from .forms import CartItemQuantityForm


# Create your views here.


class OrderItemView(APIView):
    def get(self, request, format=None):
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
    def get(self, request):
        order = Cart(request)
        return render(request, 'order.html', {'order': order})


class AddItemToOrderView(View):
    def post(self, request, product_id):
        order = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartItemQuantityForm(request.POST)
        if form.is_valid():
            # if product.warehouse > form.cleaned_data['quantity']:
            order.add(product, form.cleaned_data['quantity'])
            # else:
            #     print('nooooooooooooooooooooooooooooooo')
            return redirect('order')
        return redirect('order')


# def post(self, request, product_id):
#     order = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartItemQuantityForm(request.POST)
#     if form.is_valid():
#         if product.warehouse >= form.cleaned_data['quantity']:
#             order.add(product, form.cleaned_data['quantity'])
#             return redirect('order')
#         else:
#             print('Not enough quantity available in warehouse')
#     else:
#         print('Form is invalid')
#     return redirect('order')


class RemoveItemFromOrderView(View):
    def get(self, request, product_id):
        order = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        order.remove(product)
        return redirect('order')


class OrderDetailView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_choice')

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        address = Address.objects.filter(costumer=request.user)
        return render(request, 'order_checkout.html', {'order': order, 'addresses': address})


class OrderCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_choice')

    def get(self, request, address_id):
        cart = Cart(request)
        address = Address.objects.get(id=int(address_id))
        order = Order.objects.create(customer=request.user, address=address)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        return redirect('order-detail', order.id)


class ChooseAddressView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_choice')
    def get(self, request):
        user = request.user
        print('errorororororor')
        print(Address.objects.filter(customer_address=user).last())
        print('errorroror')
        addresses = Address.objects.filter(costumer=user)
        print(addresses)
        return render(request, "choose_address.html", {'addresses': addresses})
        # else:
        #     messages.error(request, 'you dont have any addresses please add an address first!')
        #     return redirect(reverse('profile',kwargs={'pk':user}))

    def post(self, request):
        address_id = request.POST.get('address')
        return redirect(reverse_lazy('order-create', kwargs={'address_id': address_id}))
