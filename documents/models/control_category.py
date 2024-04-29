from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel


class ControlCategory(BaseModel):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _("control category")
        verbose_name_plural = _("control categories")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("controlcategory_detail", args=(self.pk,))
