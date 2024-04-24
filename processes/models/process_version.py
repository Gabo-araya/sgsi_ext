from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.version_mixin import VersionModelBase
from documents.models.control import Control
from documents.models.document import Document
from processes.enums import TimeFrameChoices
from processes.models.process import Process


class ProcessVersion(VersionModelBase, BaseModel):
    process = models.ForeignKey(
        verbose_name=_("process"),
        to=Process,
        on_delete=models.PROTECT,
        related_name="versions",
    )
    defined_in = models.ForeignKey(
        verbose_name=_("defined in"),
        to=Document,
        on_delete=models.PROTECT,
        related_name="processes",
    )
    controls = models.ManyToManyField(
        verbose_name=_("control"),
        to=Control,
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
        return f"{self.process}  V{self.version}"

    def _get_versioned_instance(self) -> Process:
        return self.process

    def get_absolute_url(self) -> str:
        return reverse("processversion_detail", args=(self.pk,))
