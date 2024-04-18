from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel


class AssetType(BaseModel):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
    )

    class Meta:
        verbose_name = _("asset type")
        verbose_name_plural = _("asset types")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("assettype_detail", args=(self.pk,))
