from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User, Address
from config.settings import ORDER_SESSION_ID
from product.models import Product
from .cart import Cart
from .models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer, ProductSerializer


#
# class OrderItemView(ListCreateAPIView):
#     # def get(self,request ,format=None):
#     #     order_item = OrderItem.objects.all()
#     #     serilizer = OrderItemSerializer(order_item, many=True)
#     #     return Response(serilizer.data)
#     # @permission_classes([AllowAny])
#     # def post(self, request, format=None):
#     #     print(request)
#
#     permission_classes = [AllowAny]
#     serializer_class = OrderItemSerializer
#     print(serializer_class.data)
#     queryset = OrderItem.objects.all()
#
#
#
#
#         # serializer = OrderItemSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.create(serializer.validated_data)
#         #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class OrderView(APIView):
#     def get(self,request ,format=None):
#         user = request.user
#         orders = User.objects.select_related('Cart').all()
#         serilizer = OrderSerializer(orders, many=True)
#         return Response(serilizer.data)
#
#     def post(self, request, format=None):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             if request.user.is_authenticated:
#                 user=request.user
#                 Cart.objects.create(customer=user.id,
#                                      )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # class OrderView(ListCreateAPIView):
# #     permission_classes = [AllowAny]
# #     queryset = Cart.objects.all()
# #     serializer_class = OrderSerializer
#
#
# class ProductApiView(ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
class ProductAPI(APIView):
    """
    Single API to handle product operations
    """
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        qs = Product.objects.all()

        return Response(
            {"data": self.serializer_class(qs, many=True).data},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class CartApiView(APIView):

    def get(self, request, format=None):
        cart = Cart(request)
        order = request.session.get(ORDER_SESSION_ID)
        return Response(order)

    def post(self, request, format=None):
        product_id = request.data.get('product_id')
        action = request.data.get('action')
        print(type(action))
        quantity = int(request.data.get('quantity'))
        product = Product.objects.get(pk=product_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(product, quantity)
            return Response({'message': 'Product added to cart successfully'})
        elif action == 'delete':
            cart.remove(product)
            return Response({'message': 'Item was deleted successfully'})

    def delete(self, request,pk ,format=None):
        product = Product.objects.get(id=pk)
        cart = Cart(request)
        cart.remove(product)
        return Response({'message':'product was deleted successfully'})


    # def delete(self, request, format=None):
    #     product_id = request.data.get('product_id')
    #     product = Product.objects.get(pk=product_id)
    #     cart = Cart(request)
    #     cart.remove(product=product)
    #     cart.save_session()
    #     return Response({'message': 'item was deleted successfully'})


class OrderCreateApiView(APIView):
    # permission_classes = [IsAdminUser,IsAuthenticated]
    def get(self, request):
        if request.user.is_anonymous:
            return Response({"error":"anonymous"})
        elif not Order.objects.filter(customer=request.user.id).last():
            Order.objects.create(
                address=Address.objects.last(),
                customer=request.user
            )
            order = Order.objects.filter(customer=request.user.id)
            serializer = OrderSerializer(instance=order, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('viimimvkiermgvkineknv')
            order = Order.objects.filter(customer=request.user.id)
            print(order)
            serializer = OrderSerializer(instance=order, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def post(self,request):
    #     order = Order.objects.get(customer=request.user)
    #     serializer = OrderSerializer(instance=order,many=True)
    #     if serializer.is_valid():
    #         Order.objects.create(
    #             address=Address.objects.last(),
    #             customer=request.user
    #         )
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response({"ERROR":"BAD REQUEST"},status=status.HTTP_400_BAD_REQUEST)

