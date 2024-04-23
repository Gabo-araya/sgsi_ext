from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel


class ProcessActivity(BaseModel):
    process_version = models.ForeignKey(
        verbose_name=_("process version"),
        to="ProcessVersion",
        on_delete=models.CASCADE,
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

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} {self.order} for {self.process_version}"

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self._auto_increment_order()
        return super().save(*args, **kwargs)

    def _auto_increment_order(self) -> None:
        last_order = self.process_version.activities.aggregate(models.Max("order")).get(
            "order__max"
        )
        self.order = last_order + 1 if last_order is not None else 1

    def get_absolute_url(self) -> str:
        return reverse("processactivity_detail", args=(self.pk,))
