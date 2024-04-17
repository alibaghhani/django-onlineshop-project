from functools import partial

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


class Category(TimeStampMixin, LogicalDeleteMixin):
    name = models.CharField(max_length=250)


class Image(LogicalDeleteMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField
    image = models.FileField(
        upload_to=partial(maker, "images"),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "png", "jpg", "gif", "mp4", "avi", "flv"]
            )
        ],
    )
