from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from information_assets.models.asset_role import AssetRole


class AssetRoleUser(BaseModel):
    role = models.ForeignKey(
        verbose_name=_("role"),
        to=AssetRole,
        on_delete=models.CASCADE,
        related_name="asset_role_users",
    )
    user = models.ForeignKey(
        verbose_name=_("user"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="asset_role_users",
    )

    class Meta:
        verbose_name = _("asset role user")
        verbose_name_plural = _("asset role users")

    def __str__(self) -> str:
        return f"{self.role} - {self.user}"
