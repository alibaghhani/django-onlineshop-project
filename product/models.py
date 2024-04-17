from django.db import models
from core.models import TimeStampMixin,LogicalDeleteMixin

# Create your models here.
class Product(TimeStampMixin,LogicalDeleteMixin):
    name = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    title = models.TextField(max_length=250)
    category = models.ForeignKey('Category',on_delete=models.PROTECT,related_name='product_category')
