from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.control import Control
from processes.enums import TimeFrameChoices

if TYPE_CHECKING:
    from processes.models.process import Process


class ProcessDefinition(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    control = models.ForeignKey(
        to=Control,
        on_delete=models.CASCADE,
        related_name="process_definitions",
        verbose_name=_("control"),
    )
    recurrency = models.CharField(
        verbose_name=_("recurrency"),
        max_length=255,
        choices=TimeFrameChoices.choices,
        blank=True,
    )

    class Meta:
        verbose_name = _("process definition")
        verbose_name_plural = _("process definitions")

    def __str__(self) -> str:
        return self.name

    def create_activities_for_process(self, process: Process) -> None:
        for activity_definition in self.activity_definitions.all():
            activity_definition.create_activity_for_process(process)

    def get_absolute_url(self) -> str:
        return reverse("processdefinition_detail", args=(self.pk,))
