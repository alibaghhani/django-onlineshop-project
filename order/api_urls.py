from order.api_views import CartApiView,ProductAPI,OrderCreateApiView
from django.urls import path

urlpatterns = [
    path('cart/', CartApiView.as_view(), name='cart'),
    path('products/', ProductAPI.as_view(), name='products_api'),
    path('order/', OrderCreateApiView.as_view(), name='orders'),

]