from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.control import Control
from processes.enums import TimeFrameChoices

if TYPE_CHECKING:
    from processes.models.process_instance import ProcessInstance


class Process(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    control = models.ForeignKey(
        to=Control,
        on_delete=models.CASCADE,
        related_name="processes",
        verbose_name=_("control"),
    )
    recurrency = models.CharField(
        verbose_name=_("recurrency"),
        max_length=255,
        choices=TimeFrameChoices.choices,
        blank=True,
    )

    class Meta:
        verbose_name = _("process")
        verbose_name_plural = _("processes")

    def __str__(self) -> str:
        return self.name

    def create_activities_for_process_instance(
        self, process_instance: ProcessInstance
    ) -> None:
        for activity in self.activities.all():
            activity.create_activity_for_process_instance(process_instance)

    def get_absolute_url(self) -> str:
        return reverse("process_detail", args=(self.pk,))
