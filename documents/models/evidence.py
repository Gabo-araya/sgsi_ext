from __future__ import annotations

import hashlib
import os

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.html import escape
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from base.fields.base import BaseFileField
from base.models.base_model import BaseModel
from base.utils import build_absolute_url_wo_req

if TYPE_CHECKING:
    from documents.forms import EvidenceForm


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
    text = models.TextField(
        verbose_name=_("text"),
        blank=True,
    )
    shasum = models.CharField(
        verbose_name=_("shasum"),
        max_length=64,
    )

    class Meta:
        verbose_name = _("evidence")
        verbose_name_plural = _("evidences")
        constraints = (
            models.CheckConstraint(
                check=(
                    (~models.Q(file="") & models.Q(url="") & models.Q(text=""))
                    | (models.Q(file="") & ~models.Q(url="") & models.Q(text=""))
                    | (models.Q(file="") & models.Q(url="") & ~models.Q(text=""))
                ),
                name="file_url_or_text",
                violation_error_message=_(
                    "An evidence must have either a file, a url or text."
                ),
            ),
        )

    def __str__(self) -> str:
        if hasattr(self, "process_activity_instance"):
            return f"Evidence for {self.process_activity_instance}"
        if hasattr(self, "approved_document_version"):
            return f"Evidence for {self.approved_document_version}"
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

    def get_html_content(self) -> str:
        if self.file:
            url = (
                build_absolute_url_wo_req(self.file.url)
                if self.file.url.startswith("/")
                else self.file.url
            )
            return format_html(
                '<a target="_blank" href="{}">{}</a>',
                url,
                os.path.basename(self.file.name),
            )
        if self.url:
            return format_html(
                '<a target="_blank" href="{}">{}</a>', self.url, self.url
            )
        return escape(self.text)

    def get_text_content(self) -> str:
        if self.file:
            url = (
                build_absolute_url_wo_req(self.file.url)
                if self.file.url.startswith("/")
                else self.file.url
            )
            return f"{os.path.basename(self.file.name)} ({url})"
        if self.url:
            return self.url
        return self.text

    @classmethod
    def create_from_form(cls, form: type[EvidenceForm]) -> Evidence:
        if file := form.cleaned_data["evidence_file"]:
            return cls.objects.create(file=file)
        if url := form.cleaned_data["evidence_url"]:
            return cls.objects.create(url=url)
        return cls.objects.create(text=form.cleaned_data["evidence_text"])
