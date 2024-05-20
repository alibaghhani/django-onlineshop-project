from .views import AddItemToOrderView,OrderView,RemoveItemFromOrderView
from django.urls import path

urlpatterns = [
    path('orderpreview/',OrderView.as_view(),name='order'),
    path('additem/<int:product_id>/', AddItemToOrderView.as_view(), name='order-add-item'),
    path('removeitem/<int:product_id>/',RemoveItemFromOrderView.as_view(),name='order-remove-item')
    # path('api/products/', ProductApiView.as_view()),


]
