from django.db import models
from django.utils.translation import gettext_lazy as _

from api_client.enums import ClientCodes
from api_client.managers import ClientConfigQueryset
from base.models import BaseModel


class ClientConfig(BaseModel):
    """Represents an API client configuration."""

    client_code = models.CharField(
        verbose_name=_("client code"),
        max_length=255,
        choices=ClientCodes.choices,
        unique=True,
        null=False,
        blank=False,
    )
    enabled = models.BooleanField(
        verbose_name=_("enabled"),
        default=True,
    )
    retries = models.PositiveIntegerField(
        verbose_name=_("retries"),
        default=0,
    )

    objects = ClientConfigQueryset.as_manager()

    class Meta:
        verbose_name = _("client configuration")
        verbose_name_plural = _("clients configurations")

    def __str__(self) -> str:
        return (
            f"{self.client_code} - (enabled: {self.enabled}, retries: {self.retries})"
        )
