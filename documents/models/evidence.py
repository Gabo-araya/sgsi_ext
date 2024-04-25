from django.db import models
from django.utils.translation import gettext_lazy as _

from base.fields.base import BaseFileField
from base.models.base_model import BaseModel
from base.models.file_integrity_mixin import FileIntegrityModelBase


class Evidence(FileIntegrityModelBase, BaseModel):
    file = BaseFileField(
        verbose_name=_("file"),
        null=True,
        blank=True,
    )
    url = models.URLField(
        verbose_name=_("URL"),
        blank=True,
    )

    class Meta:
        verbose_name = _("evidence")
        verbose_name_plural = _("evidences")
        constraints = (
            models.CheckConstraint(
                check=models.Q(file__isnull=False) ^ models.Q(url__isnull=False),
                name="file_xor_url",
            ),
        )

    def __str__(self) -> str:
        if hasattr(self, "process_activity_instance"):
            return (
                f"Evidence for {self.document_version} - "
                f"{self.process_activity_instance}"
            )
        return f"Evidence for {self.document_version}"

    def get_absolute_url(self) -> str:
        ...
