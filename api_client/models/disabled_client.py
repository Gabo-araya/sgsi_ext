from django.db import models
from django.utils.translation import gettext_lazy as _

from api_client.enums import ClientCodes
from api_client.managers import DisabledClientQueryset


class DisabledClient(models.Model):
    disabled_at = models.DateTimeField(
        verbose_name=_("disabled at"),
        auto_now_add=True,
    )
    client_code = models.CharField(
        verbose_name=_("client code"),
        max_length=255,
        choices=ClientCodes.choices,
        unique=True,
    )

    objects = DisabledClientQueryset.as_manager()

    class Meta:
        verbose_name = _("disabled client")
        verbose_name_plural = _("disabled clients")

    def __str__(self) -> str:
        return f"{self.disabled_at} - {self.client_code}"
