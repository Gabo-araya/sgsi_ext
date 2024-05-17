from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from processes.managers import ProcessInstanceQuerySet
from processes.models.process_version import ProcessVersion


class ProcessInstance(BaseModel):
    process_version = models.ForeignKey(
        verbose_name=_("process version"),
        to=ProcessVersion,
        on_delete=models.PROTECT,
        related_name="instances",
    )
    comment = models.TextField(verbose_name=_("comment"), blank=True)
    is_completed = models.BooleanField(verbose_name=_("is completed"), default=False)
    completed_at = models.DateTimeField(
        verbose_name=_("completed at"), blank=True, null=True
    )

    objects = ProcessInstanceQuerySet.as_manager()

    class Meta:
        verbose_name = _("process instance")
        verbose_name_plural = _("process instances")

    def __str__(self) -> str:
        return f"{self.process_version} Instance"

    def save(self, *args, **kwargs) -> None:
        adding = self._state.adding
        super().save(*args, **kwargs)
        if adding:
            self.process_version.create_first_activity_instance(self)

    def get_absolute_url(self) -> str:
        return reverse("processinstance_detail", args=(self.pk,))

    def check_if_completed(self) -> None:
        if self.activity_instances.filter(is_completed=False).count() == 0:
            self.update(is_completed=True, completed_at=timezone.now())
