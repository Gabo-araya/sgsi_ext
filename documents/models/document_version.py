from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.mixins import FileIntegrityModelBase
from documents.managers import DocumentVersionQuerySet
from documents.models.document import Document
from documents.models.document_version_read_by_user import DocumentVersionReadByUser
from users.models import User


class DocumentVersion(FileIntegrityModelBase, BaseModel):
    document = models.ForeignKey(
        verbose_name=_("document"),
        to=Document,
        on_delete=models.PROTECT,
        related_name="versions",
    )
    version = models.PositiveIntegerField(
        verbose_name=_("version"),
    )
    comment = models.TextField(
        verbose_name=_("comment"),
        blank=True,
    )
    is_approved = models.BooleanField(
        verbose_name=_("is approved"),
        default=False,
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

    def __str__(self) -> str:
        return f"{self.document.title} - V{self.version}"

    @property
    def can_be_updated(self) -> bool:
        return not self.is_approved

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self._auto_increment_version()
        super().save(*args, **kwargs)

    def _auto_increment_version(self) -> None:
        last_version = self.document.versions.aggregate(models.Max("version")).get(
            "version__max"
        )
        self.version = last_version + 1 if last_version is not None else 1

    def approve(self) -> None:
        self.update(is_approved=True)

    def mark_as_read(self, user: User) -> None:
        self.read_by.add(user)

    def was_read_by_user(self, user: User) -> bool:
        return self.read_by.filter(pk=user.pk).exists()

    def get_absolute_url(self):
        return reverse("documentversion_detail", args=(self.pk,))
