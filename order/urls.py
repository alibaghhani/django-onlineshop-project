from .views import (AddItemToOrderView,OrderView,RemoveItemFromOrderView
                    ,OrderDetailView,OrderCreateView,ChooseAddressView)
from django.urls import path

urlpatterns = [
    path('orderpreview/',OrderView.as_view(),name='order'),
    path('additem/<int:product_id>/', AddItemToOrderView.as_view(), name='order-add-item'),
    path('removeitem/<int:product_id>/',RemoveItemFromOrderView.as_view(),name='order-remove-item'),
    path('ordercreate/<int:address_id>/',OrderCreateView.as_view(),name='order-create'),
    path('orderdetail/<int:order_id>',OrderDetailView.as_view(),name='order-detail'),
    path('address_choose/',ChooseAddressView.as_view(),name='choose_address')


]
