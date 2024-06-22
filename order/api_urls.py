from django.urls import path

from order.api_views import (AddressChooseAPIView, CartApiView,
                             OrderCreateApiView, ProductGenericAPI)

urlpatterns = [
    path('cart/', CartApiView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartApiView.as_view(), name='cart-api-delete'),
    path('products/', ProductGenericAPI.as_view(), name='products_api'),
    path('order/<int:address_id>/', OrderCreateApiView.as_view(), name='orders'),
    path('choose_address/', AddressChooseAPIView.as_view(), name='api_address_choose'), ]
