from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class OrderableModel(BaseModel):
    display_order = models.PositiveSmallIntegerField(
        _("display order"),
        default=0,
    )

    class Meta:
        abstract = True
        ordering = ("display_order",)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self._set_display_order()
        super().save(*args, **kwargs)

    def _set_display_order(self):
        """
        When adding a new object, set display_order field
        counting all objects plus 1
        """
        obj_count = self.__class__.objects.count()
        self.display_order = obj_count + 1

    @classmethod
    def reorder_display_order(cls):
        """
        Take all objects and change order value
        """
        objects = cls.objects.all()
        order = 0
        for obj in objects:
            obj.display_order = order
            obj.save()
            order += 1
