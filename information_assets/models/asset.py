from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from information_assets.enums import ClassificationChoices
from information_assets.enums import CriticalityChoice
from information_assets.models.asset_type import AssetType
from users.models import User


class Asset(BaseModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("owner"), related_name="assets"
    )
    name = models.CharField(verbose_name=_("name"), max_length=30)
    description = models.TextField(verbose_name=_("description"), blank=True)
    asset_type = models.ForeignKey(
        AssetType,
        on_delete=models.PROTECT,
        verbose_name=_("type"),
        related_name="assets",
    )
    criticality = models.CharField(
        verbose_name=_("criticality"), choices=CriticalityChoice.choices, max_length=9
    )
    classification = models.CharField(
        verbose_name=_("classification"),
        choices=ClassificationChoices.choices,
        max_length=10,
    )

    class Meta:
        verbose_name = _("asset")
        verbose_name_plural = _("assets")
        constraints = (
            models.UniqueConstraint(
                fields=("name", "owner"), name="unique_asset_name_owner"
            ),
        )

    def __str__(self):
        return f"{self.name} - {self.owner.get_full_name()}"

    def get_absolute_url(self):
        return reverse("asset_detail", args=(self.pk,))
