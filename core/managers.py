from django.db import models


class LogicalQuerySet(models.QuerySet):
    def undelete(self):
        return super().update(is_deleted=False)

    def delete(self):
        return super().update(is_deleted=True)

    def activate(self):
        return super().update(is_active=True)

    def deactivate(self):
        return super().update(is_active=False)


