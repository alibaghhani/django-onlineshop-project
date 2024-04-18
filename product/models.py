from functools import partial

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from core.models import TimeStampMixin, LogicalDeleteMixin
from core.utils import maker


# Create your models here.
class Product(TimeStampMixin, LogicalDeleteMixin):
    name = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    title = models.TextField(max_length=250)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='product_category')

    expired_at = None

    def __str__(self):
        return f"{self.category}----{self.name}"

class Category(TimeStampMixin, LogicalDeleteMixin):
    name = models.CharField(max_length=250)
    sub_category = models.ForeignKey('self',nullt=True,blank=True)
    expired_at = None

    def __str__(self):
        return f"{self.name}"


class Image(LogicalDeleteMixin):
    image = models.FileField(
        upload_to=partial(maker, "images"),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "png", "jpg", "gif", "mp4", "avi", "flv"]
            )
        ],
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

class Discount(TimeStampMixin):
    """
    discount model

    -----fields-----
    discount = models.PositiveIntegerField(max_length=250, blank=True, null=True, unique=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_discount')


    """
    discount = models.PositiveIntegerField( blank=True, null=True, unique=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_discount')


class DiscountCode(models.Model):
    """
    discount coupon model

    -----fields-----
        code = models.CharField(max_length=8, blank=True, null=True, unique=True)

    """

    code = models.CharField(max_length=8, blank=True, null=True, unique=True)

    def __str__(self):
        return "%s" % (self.code)

