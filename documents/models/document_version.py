from __future__ import annotations

import hashlib
import secrets
import string

from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.fields.base import BaseFileField
from base.models.base_model import BaseModel
from base.models.version_mixin import VersionModelBase
from documents.managers import DocumentVersionQuerySet
from documents.models.document import Document
from documents.models.document_version_read_by_user import DocumentVersionReadByUser
from documents.models.evidence import Evidence
from users.models.user import User

if TYPE_CHECKING:
    from documents.forms import DocumentVersionApproveForm


def generate_verification_code():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(8))


class DocumentVersion(VersionModelBase, BaseModel):
    document = models.ForeignKey(
        verbose_name=_("document"),
        to=Document,
        on_delete=models.PROTECT,
        related_name="versions",
    )
    author = models.ForeignKey(
        verbose_name=_("author"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="authored_document_versions",
        null=True,
    )
    comment = models.TextField(
        verbose_name=_("comment"),
        blank=True,
    )
    file = BaseFileField(
        verbose_name=_("file"),
        blank=True,
    )
    file_url = models.URLField(
        verbose_name=_("file url"),
        blank=True,
    )
    shasum = models.CharField(
        verbose_name=_("shasum"),
        max_length=64,
    )
    is_approved = models.BooleanField(
        verbose_name=_("is approved"),
        default=False,
    )
    approval_evidence = models.OneToOneField(
        verbose_name=_("approval evidence"),
        to="documents.Evidence",
        on_delete=models.PROTECT,
        related_name="approved_document_version",
        null=True,
        blank=True,
    )
    approved_at = models.DateTimeField(
        verbose_name=_("approved at"),
        null=True,
        blank=True,
    )
    approved_by = models.ForeignKey(
        verbose_name=_("approved by"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="approved_document_versions",
        null=True,
        blank=True,
    )
    verification_code = models.CharField(
        verbose_name=_("verification code"),
        max_length=8,
        editable=False,
        default=generate_verification_code,
    )
    read_by = models.ManyToManyField(
        verbose_name=_("read by users"),
        to=settings.AUTH_USER_MODEL,
        through=DocumentVersionReadByUser,
        through_fields=("document_version", "user"),
        related_name="read_document_versions",
    )

    objects = DocumentVersionQuerySet.as_manager()

    class Meta:
        verbose_name = _("document version")
        verbose_name_plural = _("document versions")
        ordering = ("-version",)
        constraints = (
            models.UniqueConstraint(
                fields=["document", "version"], name="unique_document_version"
            ),
            models.CheckConstraint(
                check=models.Q(file="") ^ models.Q(file_url=""),
                name="file_xor_file_url",
                violation_error_message=_("Either file or file url must be set"),
            ),
        )
        permissions = (
            ("approve_documentversion", _("Can approve document version")),
            (
                "view_documentversion_verification_code",
                _("Can view document version verification code"),
            ),
        )

    @property
    def can_be_updated(self) -> bool:
        return not self.is_approved

    def save(self, *args, **kwargs) -> None:
        self._set_shasum()
        return super().save(*args, **kwargs)

    def _set_shasum(self) -> str:
        self.shasum = (
            self.get_shasum_of_file() if self.file else self.get_shasum_of_file_url()
        )

    def get_shasum_of_file(self) -> str:
        sha256 = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

    def get_shasum_of_file_url(self) -> str:
        return hashlib.sha256(self.file_url.encode()).hexdigest()

    def __str__(self) -> str:
        return f"{self.document.title} - V{self.version}"

    def _get_increment_queryset(self) -> DocumentVersionQuerySet:
        return self.document.versions.all()

    def mark_as_approved(self, user: User, form: DocumentVersionApproveForm) -> None:
        update_dict = self.get_approve_update_dict(user)
        evidence = Evidence.create_from_form(form)
        self.update(approval_evidence=evidence, **update_dict)

    def get_approve_update_dict(self, user: User) -> None:
        update_dict = {"is_approved": True, "approved_at": timezone.now()}
        if user and not user.is_anonymous:
            update_dict["approved_by"] = user
        return update_dict

    def mark_as_read(self, user: User) -> None:
        self.read_by.add(user)

    def is_read_by_user(self, user: User) -> bool:
        return self.read_by.filter(pk=user.pk).exists()

    def get_absolute_url(self):
        return reverse(
            "documentversion_detail", args=(self.document.code, self.version)
        )
