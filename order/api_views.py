from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from product.models import Product
from .models import OrderItem,Order
from .serializers import OrderItemSerializer,OrderSerializer,ProductSerializer

class OrderItemView(ListCreateAPIView):
    # def get(self,request ,format=None):
    #     order_item = OrderItem.objects.all()
    #     serilizer = OrderItemSerializer(order_item, many=True)
    #     return Response(serilizer.data)
    # @permission_classes([AllowAny])
    # def post(self, request, format=None):
    #     print(request)

    permission_classes = [AllowAny]
    serializer_class = OrderItemSerializer
    print(serializer_class.data)
    queryset = OrderItem.objects.all()




        # serializer = OrderItemSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.create(serializer.validated_data)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderView(APIView):
    def get(self,request ,format=None):
        user = request.user
        orders = User.objects.select_related('Order').all()
        serilizer = OrderSerializer(orders, many=True)
        return Response(serilizer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                user=request.user
                Order.objects.create(customer=user.id,
                                     )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OrderView(ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


class ProductApiView(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer