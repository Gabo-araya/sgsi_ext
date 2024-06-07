from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from information_assets.models.asset import Asset


class AssetRole(BaseModel):
    asset = models.ForeignKey(
        verbose_name=_("asset"),
        to=Asset,
        on_delete=models.PROTECT,
        related_name="roles",
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    users = models.ManyToManyField(
        verbose_name=_("users"),
        to=settings.AUTH_USER_MODEL,
        through="AssetRoleUser",
        through_fields=("role", "user"),
        related_name="asset_roles",
    )

    class Meta:
        verbose_name = _("asset role")
        verbose_name_plural = _("asset roles")
        unique_together = ("asset", "name")

    def __str__(self):
        return f"{self.asset.name} - {self.name}"

    def get_absolute_url(self):
        return reverse("assetrole_detail", args=(self.pk,))
