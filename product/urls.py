from django.conf.urls.static import static
from django.urls import path

from config import settings
from .views import ProductsListView,ProductDetailView,CategoryTreeView

urlpatterns = [
   path('',ProductsListView.as_view(),name='products'),
   path('product_detail/<str:pk>',ProductDetailView.as_view(),name="product_detail"),
   path('category_tree/', CategoryTreeView.as_view(), name='category_tree'),

]
