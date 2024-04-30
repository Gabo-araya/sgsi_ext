from __future__ import annotations

import hashlib

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.fields.base import BaseFileField
from base.models.base_model import BaseModel


class Evidence(BaseModel):
    file = BaseFileField(
        verbose_name=_("file"),
        null=True,
        blank=True,
    )
    url = models.URLField(
        verbose_name=_("url"),
        blank=True,
    )
    shasum = models.CharField(verbose_name=_("shasum"), max_length=64)

    class Meta:
        verbose_name = _("evidence")
        verbose_name_plural = _("evidences")
        constraints = (
            models.CheckConstraint(
                check=(models.Q(file__isnull=True) | models.Q(file=""))
                ^ (models.Q(url__isnull=True) | models.Q(url="")),
                name="file_xor_url",
                violation_error_message=_(
                    "An evidence must have a file or a url, but not both."
                ),
            ),
        )

    def __str__(self) -> str:
        if hasattr(self, "process_activity_instance"):
            return f"Evidence for {self.process_activity_instance}"
        return "Evidence"

    def save(self, *args, **kwargs) -> None:
        self._set_shasum()
        return super().save(*args, **kwargs)

    def _set_shasum(self) -> None:
        self.shasum = (
            self.get_shasum_of_file() if self.file else self.get_shasum_of_url()
        )

    def get_shasum_of_file(self) -> str:
        sha256 = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

    def get_shasum_of_url(self) -> str:
        return hashlib.sha256(self.url.encode()).hexdigest()

    def get_absolute_url(self) -> str:
        return reverse("evidence_detail", args=(self.pk,))
