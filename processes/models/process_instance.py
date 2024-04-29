from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from processes.models.process_version import ProcessVersion


class ProcessInstance(BaseModel):
    process_version = models.ForeignKey(
        verbose_name=_("process version"),
        to=ProcessVersion,
        on_delete=models.PROTECT,
        related_name="instances",
    )
    completed = models.BooleanField(verbose_name=_("completed"), default=False)
    completed_at = models.DateTimeField(
        verbose_name=_("completed at"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("process instance")
        verbose_name_plural = _("process instances")

    def __str__(self) -> str:
        return f"{self.process_version} Instance"

    def get_absolute_url(self) -> str:
        return reverse("processinstance_detail", args=(self.pk,))

    def check_if_completed(self) -> None:
        if self.activities.filter(completed=False).count() == 0:
            self.update(completed=True, completed_at=timezone.now())
