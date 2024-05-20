from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from information_assets.enums import ClassificationChoices
from information_assets.enums import CriticalityChoices
from information_assets.managers import AssetQuerySet
from information_assets.models.asset_type import AssetType


class Asset(BaseModel):
    owner = models.ForeignKey(
        verbose_name=_("owner"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assets",
    )
    code = models.CharField(
        verbose_name=_("code"),
        max_length=20,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=63,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
    )
    asset_type = models.ForeignKey(
        verbose_name=_("type"),
        to=AssetType,
        on_delete=models.PROTECT,
        related_name="assets",
    )
    criticality = models.CharField(
        verbose_name=_("criticality"),
        choices=CriticalityChoices.choices,
        max_length=9,
    )
    classification = models.CharField(
        verbose_name=_("classification"),
        choices=ClassificationChoices.choices,
        max_length=10,
    )
    is_archived = models.BooleanField(
        verbose_name=_("is archived"),
        default=False,
    )

    objects = AssetQuerySet.as_manager()

    class Meta:
        verbose_name = _("asset")
        verbose_name_plural = _("assets")
        ordering = ("code",)
        constraints = (
            models.UniqueConstraint(
                fields=("code", "owner"), name="unique_asset_owner"
            ),
        )
        permissions = (("archive_asset", _("Can archive asset")),)

    def __str__(self):
        return f"{self.name} - {self.owner.get_full_name()}"

    def get_absolute_url(self):
        return reverse("asset_detail", args=(self.pk,))

    def toggle_archive(self) -> None:
        self.update(is_archived=not self.is_archived)
