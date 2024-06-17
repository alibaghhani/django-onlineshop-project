from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models

from account.models import User
from core.models import TimeStampMixin, LogicalDeleteMixin


class Product(TimeStampMixin, LogicalDeleteMixin):
    """
    product model for save products
    """
    name = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    detail = models.TextField(max_length=250)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='product_category')
    warehouse = models.PositiveIntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    expired_at = None

    @property
    def discounted_price(self):
        discounts = self.product_discount.all()
        for discount in discounts:
            if discount.type_of_discount == 'percentage':
                discounted_price = self.price * discount.discount / 100
            else:
                discounted_price = self.price - discount.discount
            return discounted_price

    def get_warehouse(self):
        if self.warehouse == 1:
            return True
        else:
            return False

    # override save method to create slug fr products
    def save(self, *args, **kwargs):
        self.slug = f"{self.name.replace(' ', '-')}-{self.id}-{self.category}"
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.category}----{self.name}"


class Category(TimeStampMixin, LogicalDeleteMixin):
    """
    category model for creating category
    """
    name = models.CharField(max_length=250)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="child")
    expired_at = None

    def get_all_parents(self):
        return Category.objects.filter(parent_id=None)

    def __str__(self):
        return f"{self.name}"


class Image(LogicalDeleteMixin):
    image = models.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "png", "jpg", "gif", "mp4", "avi", "flv"]
            )
        ],
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_post')

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type','object_id')


class Discount(TimeStampMixin, LogicalDeleteMixin):
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
    type_of_discount = models.CharField(choices=DISCOUNT_CHOICES, max_length=250, null=True, blank=True)
    discount = models.PositiveIntegerField(blank=True, null=True, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_discount')



class DiscountCode(models.Model):
    """
    discount coupon model

    -----fields-----
        code = models.CharField(max_length=8, blank=True, null=True, unique=True)

    """

    code = models.CharField(max_length=8, blank=True, null=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_discount_code')

    def __str__(self):
        return "%s" % (self.code)
