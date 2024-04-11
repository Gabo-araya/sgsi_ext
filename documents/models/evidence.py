from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.mixins import FileIntegrityModelBase
from processes.models.process_activity import ProcessActivity


class Evidence(FileIntegrityModelBase, BaseModel):
    document_version = models.ForeignKey(
        verbose_name=_("document version"),
        to="DocumentVersion",
        on_delete=models.PROTECT,
        related_name="evidences",
    )
    activity = models.ForeignKey(
        verbose_name=_("activity"),
        to=ProcessActivity,
        on_delete=models.PROTECT,
        related_name="evidences",
    )

    class Meta:
        verbose_name = _("evidence")
        verbose_name_plural = _("evidences")

    def __str__(self) -> str:
        return f"Evidence for {self.document_version} - {self.activity}"

    def get_absolute_url(self) -> str:
        ...
