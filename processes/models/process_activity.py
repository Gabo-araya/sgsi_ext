from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from inflection import ordinal

from base.models.base_model import BaseModel
from base.models.increment_field_mixin import IncrementFieldModelBase
from users.models.group import Group

if TYPE_CHECKING:
    from processes.models.process_instance import ProcessInstance
    from users.models.user import User


class ProcessActivity(IncrementFieldModelBase, BaseModel):
    process_version = models.ForeignKey(
        verbose_name=_("process version"),
        to="ProcessVersion",
        on_delete=models.PROTECT,
        related_name="activities",
    )
    order = models.PositiveIntegerField(verbose_name=_("order"))
    description = models.TextField(verbose_name=_("description"))
    assignee_group = models.ForeignKey(
        verbose_name=_("assignee group"),
        to=Group,
        on_delete=models.PROTECT,
        related_name="activities",
    )
    email_to_notify = models.EmailField(
        verbose_name=_("email to notify"),
        blank=True,
    )

    class Meta:
        verbose_name = _("process activity")
        verbose_name_plural = _("process activities")
        ordering = ("process_version", "order")

    @property
    def can_be_updated(self) -> bool:
        return self.process_version.can_be_updated

    def __str__(self) -> str:
        return f"{self.order}{ordinal(self.order)} Activity of {self.process_version}"

    def _get_increment_queryset(self) -> models.QuerySet[ProcessActivity]:
        return self.process_version.activities.all()

    def _get_field_to_increment(self) -> str:
        return "order"

    def create_instance(
        self, process_instance: ProcessInstance, assignee: User | None = None
    ) -> None:
        from processes.models.process_activity_instance import ProcessActivityInstance

        if assignee is None:
            assignee = process_instance.created_by
        ProcessActivityInstance.objects.create(
            process_instance=process_instance,
            activity=self,
            assignee=assignee,
        )

    def get_next_activity(self) -> ProcessActivity | None:
        return self.process_version.activities.filter(order=self.order + 1).first()

    def get_absolute_url(self) -> str:
        return reverse("processactivity_detail", args=(self.pk,))
