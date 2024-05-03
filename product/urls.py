from django.conf.urls.static import static
from django.urls import path

from config import settings
from .views import ProductsListView,ProductDetailView

urlpatterns = [
   path('',ProductsListView.as_view(),name='products'),
   path('product_detail/<str:pk>',ProductDetailView.as_view(),name="product_detail")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
