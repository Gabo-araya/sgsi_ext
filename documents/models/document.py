from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from base.models.versionable_mixin import VersionableMixin

if TYPE_CHECKING:
    from documents.models.document_version import DocumentVersion


class Document(VersionableMixin, BaseModel):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
    )

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")

    def __str__(self) -> str:
        return self.title

    @property
    def last_approved_version(self) -> DocumentVersion | None:
        return self.versions.approved().order_by("-version").first()

    @property
    def can_add_new_versions(self) -> bool:
        return not self.versions.not_approved().exists()

    def get_absolute_url(self) -> str:
        return reverse("document_detail", args=(self.pk,))
