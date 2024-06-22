from django.db import models

from account.models import Address, User
from core.models import LogicalDeleteMixin, TimeStampMixin
from product.models import Discount as DiscountModel
from product.models import Product as ProductModel


class Order(TimeStampMixin, LogicalDeleteMixin):
    """
    order model for saving users orders

    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_order')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='customer_address')
    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def get_total_price(self):
        return sum(order_item.get_total_price() for order_item in self.order_items.all())


class OrderItem(TimeStampMixin, LogicalDeleteMixin):
    """
    order-item model for saving users order items
    """
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product_order')
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    price = models.PositiveIntegerField()

    def get_total_price(self):
        return self.price * self.quantity

    @property
    def discount(self):
        return DiscountModel.objects.filter(product=self.product)

    def discounted_price(self):
        if self.discount:
            return self.get_total_price() - (self.quantity * self.discount)
        else:
            return None
