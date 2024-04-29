from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.evidence import Evidence
from processes.models.process_activity import ProcessActivity
from processes.models.process_instance import ProcessInstance


class ProcessActivityInstance(BaseModel):
    process_instance = models.ForeignKey(
        verbose_name=_("process instance"),
        to=ProcessInstance,
        on_delete=models.PROTECT,
        related_name="activity_instances",
    )
    activity = models.ForeignKey(
        verbose_name=_("activity"),
        to=ProcessActivity,
        on_delete=models.PROTECT,
        related_name="activity_instances",
    )
    asignee = models.ForeignKey(
        verbose_name=_("asignee"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="activity_instances",
    )
    completed = models.BooleanField(
        verbose_name=_("completed"),
        default=False,
    )
    completed_at = models.DateTimeField(
        verbose_name=_("completed at"),
        null=True,
        blank=True,
    )
    evidence = models.OneToOneField(
        verbose_name=_("evidence"),
        to=Evidence,
        on_delete=models.PROTECT,
        related_name="process_activity_instance",
        null=True,
    )

    class Meta:
        verbose_name = _("process activity instance")
        verbose_name_plural = _("process activity instances")

    def __str__(self) -> str:
        return f"{self.process_instance} - {self.activity}"

    def get_absolute_url(self) -> str:
        return reverse("processactivityinstance_detail", args=(self.pk,))

    def mark_as_completed(self) -> None:
        self.update(completed=True, completed_at=timezone.now())
        self.process_instance.check_if_completed()
