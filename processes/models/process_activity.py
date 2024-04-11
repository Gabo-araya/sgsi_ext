from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.document_version import DocumentVersion
from processes.models.process import Process
from processes.models.process_activity_definition import ProcessActivityDefinition
from users.models import User


class ProcessActivity(BaseModel):
    process = models.ForeignKey(
        to=Process,
        on_delete=models.PROTECT,
        related_name="activities",
        verbose_name=_("process"),
    )
    activity_definition = models.ForeignKey(
        to=ProcessActivityDefinition,
        on_delete=models.PROTECT,
        related_name="activities",
        verbose_name=_("activity definition"),
    )
    order = models.PositiveIntegerField(verbose_name=_("order"))
    description = models.TextField(verbose_name=_("description"))
    asignee = models.ForeignKey(
        verbose_name=_("asignee"),
        to=User,
        on_delete=models.PROTECT,
        related_name="activities",
    )
    asignee_group = models.ForeignKey(
        verbose_name=_("asignee group"),
        to=Group,
        on_delete=models.PROTECT,
        related_name="activities",
        null=True,
        blank=True,
    )
    completed = models.BooleanField(verbose_name=_("completed"), default=False)
    completed_by = models.ForeignKey(
        verbose_name=_("completed by"),
        to=User,
        on_delete=models.PROTECT,
        related_name="completed_activities",
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        verbose_name=_("completed at"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("process activity")
        verbose_name_plural = _("process activities")

    def __str__(self) -> str:
        return f"{self.process} - {self.activity_definition}"

    def get_absolute_url(self) -> str:
        return reverse("processactivity_detail", args=(self.pk,))

    def mark_as_completed(self, completed_by: User) -> None:
        self.update(
            completed=True, completed_by=completed_by, completed_at=timezone.now()
        )
        self.process.check_if_completed()

    def get_latest_document_version(self) -> DocumentVersion:
        return self.process.get_latest_document_version()
