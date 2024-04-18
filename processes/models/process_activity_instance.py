from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.document_version import DocumentVersion
from processes.models.process_activity import ProcessActivity
from processes.models.process_instance import ProcessInstance
from users.models import User


class ProcessActivityInstance(BaseModel):
    process_instance = models.ForeignKey(
        to=ProcessInstance,
        on_delete=models.PROTECT,
        related_name="activity_instances",
        verbose_name=_("process instance"),
    )
    activity = models.ForeignKey(
        to=ProcessActivity,
        on_delete=models.PROTECT,
        related_name="activity_instances",
        verbose_name=_("activity"),
    )
    order = models.PositiveIntegerField(verbose_name=_("order"))
    description = models.TextField(verbose_name=_("description"))
    asignee = models.ForeignKey(
        verbose_name=_("asignee"),
        to=User,
        on_delete=models.PROTECT,
        related_name="activity_instances",
    )
    asignee_group = models.ForeignKey(
        verbose_name=_("asignee group"),
        to=Group,
        on_delete=models.PROTECT,
        related_name="activity_instances",
        null=True,
        blank=True,
    )
    completed = models.BooleanField(verbose_name=_("completed"), default=False)
    completed_at = models.DateTimeField(
        verbose_name=_("completed at"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("process activity instance")
        verbose_name_plural = _("process activity instances")

    def __str__(self) -> str:
        return f"{self.process_instance} - {self.activity}"

    def get_absolute_url(self) -> str:
        return reverse("processactivityinstanceinstance_detail", args=(self.pk,))

    def mark_as_completed(self) -> None:
        self.update(completed=True, completed_at=timezone.now())
        self.process_instance.check_if_completed()

    def get_latest_document_version(self) -> DocumentVersion:
        return self.process_instance.get_latest_document_version()
