from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.control import Control
from documents.models.document_version import DocumentVersion
from processes.models.process_definition import ProcessDefinition


class ProcessInstance(BaseModel):
    process_definition = models.ForeignKey(
        verbose_name=_("process definition"),
        to=ProcessDefinition,
        on_delete=models.CASCADE,
        related_name="processes",
    )
    name = models.CharField(verbose_name=_("name"), max_length=255)
    control = models.ForeignKey(
        to=Control,
        on_delete=models.CASCADE,
        related_name="processes",
        verbose_name=_("control"),
    )
    completed = models.BooleanField(verbose_name=_("completed"), default=False)
    completed_at = models.DateTimeField(
        verbose_name=_("completed at"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("process instance")
        verbose_name_plural = _("process instances")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self.set_attributes_from_definition()
            super().save(*args, **kwargs)
            self.process_definition.create_activities_for_process_instance(self)
        else:
            super().save(*args, **kwargs)

    def set_attributes_from_definition(self) -> None:
        self.name = self.process_definition.name
        self.control = self.process_definition.control

    def get_absolute_url(self) -> str:
        return reverse("processinstance_detail", args=(self.pk,))

    def check_if_completed(self) -> None:
        if self.activities.filter(completed=False).count() == 0:
            self.update(completed=True, completed_at=timezone.now())

    def get_latest_document_version(self) -> DocumentVersion:
        return self.control.get_latest_document_version()
