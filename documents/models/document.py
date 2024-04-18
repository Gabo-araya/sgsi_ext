from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel

if TYPE_CHECKING:
    import datetime

    from documents.models.document_version import DocumentVersion


class Document(BaseModel):
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
    def last_version(self) -> DocumentVersion | None:
        return self.versions.order_by("-version").first()

    @property
    def last_approved_version(self) -> DocumentVersion | None:
        return self.versions.approved().order_by("-version").first()

    @property
    def latest_update(self) -> datetime.datetime:
        return max(self.updated_at, self.versions.latest("updated_at").updated_at)

    @property
    def latest_updator(self) -> datetime.datetime:
        return max(
            self, self.versions.latest("updated_at"), key=lambda x: x.updated_at
        ).updated_by

    @property
    def can_add_new_versions(self) -> bool:
        return not self.versions.not_approved().exists()

    def get_absolute_url(self) -> str:
        return reverse("document_detail", args=(self.pk,))
