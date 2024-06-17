from order.api_views import CartApiView, ProductGenericAPI, OrderCreateApiView, AddressChooseAPIView, PaymentsAPIView
from django.urls import path

urlpatterns = [
    path('cart/', CartApiView.as_view(), name='cart'),
    path('products/', ProductGenericAPI.as_view(), name='products_api'),
    path('order/<int:address_id>/', OrderCreateApiView.as_view(), name='orders'),
    path('choose_address/', AddressChooseAPIView.as_view(), name='api_address_choose'),
    path('payment/',PaymentsAPIView.as_view(),name='api-payment'),
]