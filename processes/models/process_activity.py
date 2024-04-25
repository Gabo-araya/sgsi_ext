from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from inflection import ordinal

from base.models.base_model import BaseModel
from base.models.increment_field_mixin import IncrementFieldModelBase


class ProcessActivity(IncrementFieldModelBase, BaseModel):
    process_version = models.ForeignKey(
        verbose_name=_("process version"),
        to="ProcessVersion",
        on_delete=models.PROTECT,
        related_name="activities",
    )
    order = models.PositiveIntegerField(verbose_name=_("order"))
    description = models.TextField(verbose_name=_("description"))
    asignee = models.ForeignKey(
        verbose_name=_("asignee"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="activities",
        null=True,
        blank=True,
    )
    asignee_group = models.ForeignKey(
        verbose_name=_("asignee group"),
        to=Group,
        on_delete=models.PROTECT,
        related_name="activities",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("process activity")
        verbose_name_plural = _("process activities")
        ordering = ("process_version", "order")
        constraints = (
            models.CheckConstraint(
                check=(
                    models.Q(asignee__isnull=False)
                    ^ models.Q(asignee_group__isnull=False)
                ),
                name="asignee_xor_asignee_group",
                violation_error_message=_(
                    "An activity must have an asignee or an asignee group, "
                    "but not both."
                ),
            ),
        )

    @property
    def can_be_updated(self) -> bool:
        return self.process_version.can_be_updated

    def __str__(self) -> str:
        return f"{self.order}{ordinal(self.order)} Activity of {self.process_version}"

    def _get_increment_queryset(self) -> models.QuerySet[ProcessActivity]:
        return self.process_version.activities.all()

    def _get_field_to_increment(self) -> str:
        return "order"

    def get_absolute_url(self) -> str:
        return reverse("processactivity_detail", args=(self.pk,))
