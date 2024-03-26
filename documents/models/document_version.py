import hashlib

from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.fields.base import BaseFileField
from base.models.base_model import BaseModel
from documents.managers import DocumentVersionQuerySet
from documents.models.document import Document
from documents.models.document_read_by_user import DocumentReadByUser
from documents.tasks import calculate_shasum_for_document_version
from users.models import User


class DocumentVersion(BaseModel):
    document = models.ForeignKey(
        Document,
        verbose_name=_("document"),
        related_name="versions",
        on_delete=models.CASCADE,
    )
    version = models.PositiveIntegerField(verbose_name=_("version"))
    file = BaseFileField(verbose_name=_("file"))
    shasum = models.CharField(verbose_name=_("shasum"), max_length=255)
    is_approved = models.BooleanField(verbose_name=_("is approved"), default=False)
    read_by = models.ManyToManyField(
        User,
        verbose_name=_("read by users"),
        related_name="read_document_versions",
        through=DocumentReadByUser,
    )

    objects = models.Manager.from_queryset(DocumentVersionQuerySet)()

    class Meta:
        verbose_name = _("document version")
        verbose_name_plural = _("document versions")

    def __str__(self) -> str:
        return f"{self.document.title} - V{self.version}"

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self._auto_increment_version()
        super().save(*args, **kwargs)
        calculate_shasum_for_document_version.delay(self.pk)

    def _auto_increment_version(self) -> None:
        last_version = self.document.versions.aggregate(Max("version")).get(
            "version__max"
        )
        self.version = last_version + 1 if last_version is not None else 1

    def get_shasum_of_file(self) -> str:
        sha256 = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

    def get_absolute_url(self):
        return reverse("documentversion_detail", args=(self.pk,))
