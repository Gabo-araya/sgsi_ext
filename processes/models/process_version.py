from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.control import Control
from processes.enums import TimeFrameChoices

if TYPE_CHECKING:
    pass


class ProcessVersion(BaseModel):
    control = models.ForeignKey(
        verbose_name=_("control"),
        to=Control,
        on_delete=models.PROTECT,
        related_name="process_versions",
    )
    recurrency = models.CharField(
        verbose_name=_("recurrency"),
        max_length=255,
        choices=TimeFrameChoices.choices,
        blank=True,
    )

    class Meta:
        verbose_name = _("process version")
        verbose_name_plural = _("process versions")

    def __str__(self) -> str:
        # TODO: implement
        return ""

    def get_absolute_url(self) -> str:
        return reverse("processversion_detail", args=(self.pk,))
