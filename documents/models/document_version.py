from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.mixins import FileIntegrityModelBase
from documents.managers import DocumentVersionQuerySet
from documents.models.document import Document
from documents.models.document_read_by_user import DocumentReadByUser
from users.models import User


class DocumentVersion(FileIntegrityModelBase, BaseModel):
    document = models.ForeignKey(
        verbose_name=_("document"),
        to=Document,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    version = models.PositiveIntegerField(verbose_name=_("version"))
    is_approved = models.BooleanField(verbose_name=_("is approved"), default=False)
    read_by = models.ManyToManyField(
        verbose_name=_("read by users"),
        to=User,
        through=DocumentReadByUser,
        related_name="read_document_versions",
    )

    objects = models.Manager.from_queryset(DocumentVersionQuerySet)()

    class Meta:
        verbose_name = _("document version")
        verbose_name_plural = _("document versions")
        ordering = ("-version",)

    def __str__(self) -> str:
        return f"{self.document.title} - V{self.version}"

    @property
    def can_be_updated(self) -> bool:
        return not self.is_approved

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self._auto_increment_version()
        self._set_shasum_of_file()
        super().save(*args, **kwargs)

    def _auto_increment_version(self) -> None:
        last_version = self.document.versions.aggregate(models.Max("version")).get(
            "version__max"
        )
        self.version = last_version + 1 if last_version is not None else 1

    def get_absolute_url(self):
        return reverse("documentversion_detail", args=(self.pk,))
