from django.db import models

from core.managers import LogicalManager


# Create your models here.
class TimeStampMixin(models.Model):
    """
    timestamp mixin model for adding fields that related to time

    -----fields-----
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    expired_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class LogicalDeleteMixin(models.Model):
    """
    logical delete mixin for soft delete


    -----field-----
    is_active = models.BooleanField()
    is_deleted = models.BooleanField()
    """
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    objects = LogicalManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    class Meta:
        abstract = True
