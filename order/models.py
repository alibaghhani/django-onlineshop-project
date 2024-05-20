from django.db import models
from core.models import TimeStampMixin, LogicalDeleteMixin
from product.models import Product as ProductModel, Discount as DiscountModel
from account.models import User, Address


class OrderItem(TimeStampMixin, LogicalDeleteMixin):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product_order')
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items',null=True,blank=True)
    # final_price = models.PositiveIntegerField()

    @property
    def price(self):
        return self.product.price


    def get_total_price(self):
        return self.price * self.quantity

    @property
    def discount(self):
        return DiscountModel.objects.filter(product=self.product)



    def discounted_price(self):
        # return *[self.total_price()-(self.quantity*Discount.objects.filter(product=self.product)) if Discount.objects.filter(product=self.product)]
        if self.discount:
            return self.total_price - (self.quantity * self.discount)
        else:
            return None

    # def __str__(self):
    #     return f"{self.order}"


class Order(TimeStampMixin, LogicalDeleteMixin):
    # DISCOUNT_CHOICES = (
    #     ('percentage', '%'),
    #     ('cash', '$')
    # )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_order')
    address = models.ForeignKey(Address,on_delete=models.PROTECT,related_name='customer_address')
    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    # objects = add a manager to filter the chosen user's address

    # discount = models.CharField(choices=DISCOUNT_CHOICES, max_length=250, null=True, blank=True)
    #
    # def get_final_price(self):
    #     return self.order_item.all()

    def get_total_price(self):
        return sum(order_item.get_total_price() for order_item in self.order_items.all())
