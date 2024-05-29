from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from .views import ProductsListView,ProductDetailView,CategoryTreeView,SubcategoryAndProducts

urlpatterns = [
   path('',ProductsListView.as_view(),name='products'),
   path('product_detail/<str:slug>',ProductDetailView.as_view(),name="product_detail"),
   path('category_tree/', CategoryTreeView.as_view(), name='category_tree'),
   path('product_category/<int:id>/', SubcategoryAndProducts.as_view(), name='category_product'),

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

