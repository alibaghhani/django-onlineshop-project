from functools import partial
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from account.models import User
from core.models import TimeStampMixin, LogicalDeleteMixin
# from core.utils import maker
from config import  settings
# Create your models here.
class Product(TimeStampMixin, LogicalDeleteMixin):
    name = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    title = models.TextField(max_length=250)
    category = models.ForeignKey('Category',on_delete=models.PROTECT, related_name='product_category')
    # left = models.PositiveIntegerField()

    expired_at = None

    # @property
    # def discounted_price(self):
    #     if self.product_discount:
    #         discount_available = Discount.objects.filter(product=self.name)
    #         if discount_available.exists():
    #             if discount_available.filter(type_of_discount='%'):
    #                 discount.get
    #                 final_price = self.price *

    @property
    def discounted_price(self):
        discounts = self.product_discount.all()
        discounted_price = self.price
        for discount in discounts:
            if discount.type_of_discount == 'percentage':
                discounted_price -= (self.price * discount.discount) / 100
            elif discount.type_of_discount == 'cash':
                discounted_price -= discount.discount
        return discounted_price



    def __str__(self):
        return f"{self.category}----{self.name}"

class Category(TimeStampMixin, LogicalDeleteMixin):
    name = models.CharField(max_length=250)
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    expired_at = None

    def __str__(self):
        return f"{self.name}"


class Image(LogicalDeleteMixin):
    image = models.ImageField(
        upload_to='images',
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "png", "jpg", "gif", "mp4", "avi", "flv"]
            )
        ],
    )

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='products_post')

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type','object_id')

class Discount(TimeStampMixin,LogicalDeleteMixin):
    """
    discount model

    -----fields-----
    discount = models.PositiveIntegerField(max_length=250, blank=True, null=True, unique=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_discount')


    """
    DISCOUNT_CHOICES = (
        ('percentage', '%'),
        ('cash', '$')
    )
    type_of_discount = models.CharField(choices=DISCOUNT_CHOICES,max_length=250,null=True,blank=True)
    discount = models.PositiveIntegerField( blank=True, null=True, unique=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_discount')


    # def get_discount_amount(self):



class DiscountCode(models.Model):
    """
    discount coupon model

    -----fields-----
        code = models.CharField(max_length=8, blank=True, null=True, unique=True)

    """

    code = models.CharField(max_length=8, blank=True, null=True, unique=True)
    order = models.OneToOneField(settings.ORDER_MODEL,on_delete=models.CASCADE,null=True,blank=True,related_name='order_discount_code')
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user_discount_code')

    def __str__(self):
        return "%s" % (self.code)

