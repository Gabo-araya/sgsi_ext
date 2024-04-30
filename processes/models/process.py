from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.versionable_mixin import VersionableMixin
from processes.managers import ProcessQuerySet

if TYPE_CHECKING:
    from processes.models.process_version import ProcessVersion


class Process(VersionableMixin, BaseModel):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    objects = ProcessQuerySet.as_manager()

    class Meta:
        verbose_name = _("process")
        verbose_name_plural = _("processes")

    @property
    def last_published_version(self) -> ProcessVersion | None:
        return self.versions.published().order_by("-version").first()

    @property
    def can_add_new_versions(self) -> bool:
        return not self.versions.not_published().exists()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("process_detail", args=(self.pk,))
