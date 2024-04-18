from django.db import models
from core.models import TimeStampMixin,LogicalDeleteMixin
from product.models import Product
from account.models import User
# Create your models here.
class OrderItem(TimeStampMixin,LogicalDeleteMixin):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product-order')
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    order = models.ForeignKey('Order',on_delete=models.CASCADE)

    def get_total_price(self):
        return self.price * self.quantity

    # def __str__(self):
    #     return f"{self.order}"


