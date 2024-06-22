from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Address
from account.serializers import AddressSerializer
from config.settings import ORDER_SESSION_ID
from product.models import Product

from .cart import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, ProductSerializer


class ProductGenericAPI(ListCreateAPIView):
    """
    Single API to handle product operations
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ---- cart api view for displaying cart and adding items to cart
class CartApiView(APIView):

    def get(self, request):
        order = request.session.get(ORDER_SESSION_ID)
        return Response(order)

    def post(self, request):
        product_id = request.data.get('product_id')
        action = request.data.get('action')
        quantity = int(request.data.get('quantity'))
        product = Product.objects.get(pk=product_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(product, quantity)
            return Response({'message': 'Product added to cart successfully'})
        elif action == 'delete':
            cart.remove(product)
            return Response({'message': 'Item was deleted successfully'})
        elif action == 'decrease':
            cart.decrease_quantity(product_id, quantity)
            return Response({'new information was replaced'})

    def delete(self, request, pk):
        product = Product.objects.get(id=pk)
        cart = Cart(request)
        cart.remove(product)
        return Response({'message': 'product was deleted successfully'})


# ---- order api view for creating and displaying order and order-item object from cart ----
class OrderCreateApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, address_id):
        if request.user.is_anonymous:
            return Response({"error": "anonymous"})
        elif not Order.objects.filter(customer=request.user.id, is_paid=True).last():

            address_instance = Address.objects.get(id=int(address_id))
            Order.objects.create(
                address=address_instance,
                customer=request.user
            )

            order = Order.objects.filter(customer=request.user.id)
            serializer = OrderSerializer(instance=order, many=True)
            keys = [int(i) for i in list(request.session.get(ORDER_SESSION_ID).keys())]
            for product in keys:
                OrderItem.objects.create(
                    product=Product.objects.get(id=str(product)),
                    quantity=request.session.get(ORDER_SESSION_ID).get(str(product)).get('quantity'),
                    price=request.session.get(ORDER_SESSION_ID).get(str(product)).get('price'),
                    order=order.last()

                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            order = Order.objects.filter(customer=request.user.id)
            if Order.objects.filter(address=address_id).exists():
                keys = [int(i) for i in list(request.session.get(ORDER_SESSION_ID).keys())]
                for product in keys:
                    if OrderItem.objects.filter(product=keys[-1], order=order.last()).exists():
                        serializer = OrderSerializer(instance=order, many=True)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    elif not OrderItem.objects.filter(product=product, order=order.last()).exists():
                        OrderItem.objects.create(
                            product=Product.objects.get(id=product),
                            quantity=request.session.get(ORDER_SESSION_ID).get(str(product)).get('quantity'),
                            price=request.session.get(ORDER_SESSION_ID).get(str(product)).get('price'),
                            order=order.last()

                        )
                order = Order.objects.filter(customer=request.user.id)
                serializer = OrderSerializer(instance=order, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                Order.objects.filter(customer=request.user.id).update(address=address_id)
                order = Order.objects.filter(customer=request.user.id)
                serializer = OrderSerializer(instance=order, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---- api address view for choosing address ----
class AddressChooseAPIView(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        address = Address.objects.filter(costumer=request.user.id)
        serializer = AddressSerializer(instance=address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        address_id = request.data.get('address')
        try:
            address_instance = Address.objects.get(id=address_id)
            print(f"address instance:{address_instance}")
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        return HttpResponseRedirect(reverse("orders", kwargs={"address_id": address_id}))
