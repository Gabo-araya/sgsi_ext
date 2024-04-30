from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.evidence import Evidence
from processes.managers import ProcessActivityInstanceQuerySet
from processes.models.process_activity import ProcessActivity
from processes.models.process_instance import ProcessInstance

if TYPE_CHECKING:
    from processes.forms import ProcessActivityInstanceCompleteForm


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
    is_completed = models.BooleanField(
        verbose_name=_("is completed"),
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

    objects = ProcessActivityInstanceQuerySet.as_manager()

    class Meta:
        verbose_name = _("process activity instance")
        verbose_name_plural = _("process activity instances")

    def __str__(self) -> str:
        return f"{self.process_instance} - {self.activity}"

    def get_next_activity(self) -> ProcessActivity | None:
        return self.activity.get_next_activity()

    def get_absolute_url(self) -> str:
        return reverse("processactivityinstance_detail", args=(self.pk,))

    def mark_as_completed(self, form: ProcessActivityInstanceCompleteForm) -> None:
        evidence = self.create_evidence(form)
        self.create_next_activity_instance_if_exists(form)
        self.update(evidence=evidence, is_completed=True, completed_at=timezone.now())
        self.process_instance.check_if_completed()

    def create_evidence(self, form: ProcessActivityInstanceCompleteForm) -> Evidence:
        file = form.cleaned_data["evidence_file"]
        if file:
            return Evidence.objects.create(file=file)
        url = form.cleaned_data["evidence_url"]
        return Evidence.objects.create(url=url)

    def create_next_activity_instance_if_exists(
        self, form: ProcessActivityInstanceCompleteForm
    ) -> None:
        next_activity = self.get_next_activity()
        if next_activity is None:
            return
        next_activity.create_instance(
            process_instance=self.process_instance,
            asignee=form.cleaned_data["next_activity_asignee"],
        )
