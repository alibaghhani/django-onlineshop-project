from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from account.models import Address
from product.models import Product
from .cart import Cart
from .forms import CartItemQuantityForm
from .models import OrderItem, Order


# order view to display cart
class OrderView(View):
    def get(self, request):
        order = Cart(request)
        return render(request, 'order.html', {'order': order})


# AddItemToOrderView view for creating cart for users and add items to cart
class AddItemToOrderView(View):
    def post(self, request, product_id):
        order = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartItemQuantityForm(request.POST)
        if form.is_valid():
            order.add(product, form.cleaned_data['quantity'])
            return redirect('order')
        return redirect('order')


# Remove items from cart
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


# creating order item object from cart
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


# choose address view for users to choose their addresses
class ChooseAddressView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_choice')

    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(costumer=user)
        print(addresses)
        return render(request, "choose_address.html", {'addresses': addresses})

    def post(self, request):
        address_id = request.POST.get('address')
        print(address_id)
        return redirect(reverse_lazy('order-create', kwargs={'address_id': address_id}))
