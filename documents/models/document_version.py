from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.file_integrity_mixin import FileIntegrityModelBase
from base.models.version_mixin import VersionModelBase
from documents.managers import DocumentVersionQuerySet
from documents.models.document import Document
from documents.models.document_version_read_by_user import DocumentVersionReadByUser
from users.models import User


class DocumentVersion(VersionModelBase, FileIntegrityModelBase, BaseModel):
    document = models.ForeignKey(
        verbose_name=_("document"),
        to=Document,
        on_delete=models.PROTECT,
        related_name="versions",
    )
    comment = models.TextField(
        verbose_name=_("comment"),
        blank=True,
    )
    is_approved = models.BooleanField(
        verbose_name=_("is approved"),
        default=False,
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
        )
        permissions = (("approve_documentversion", _("Can approve document version")),)

    @property
    def can_be_updated(self) -> bool:
        return not self.is_approved

    def __str__(self) -> str:
        return f"{self.document.title} - V{self.version}"

    def _get_increment_queryset(self) -> DocumentVersionQuerySet:
        return self.document.versions.all()

    def approve(self, user: User) -> None:
        update_dict = {"is_approved": True, "approved_at": timezone.now()}
        if user and not user.is_anonymous:
            update_dict["approved_by"] = user
        self.update(**update_dict)

    def mark_as_read(self, user: User) -> None:
        self.read_by.add(user)

    def was_read_by_user(self, user: User) -> bool:
        return self.read_by.filter(pk=user.pk).exists()

    def get_absolute_url(self):
        return reverse("documentversion_detail", args=(self.pk,))
