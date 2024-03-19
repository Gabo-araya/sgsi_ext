from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.fields.base import BaseFileField
from base.models.base_model import BaseModel
from documents.models.document import Document
from documents.models.document_read_by_user import DocumentReadByUser
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

    class Meta:
        verbose_name = _("document version")
        verbose_name_plural = _("document versions")

    def __str__(self):
        return f"{self.document.title} - V{self.version}"

    def get_absolute_url(self):
        return reverse("documentversion_detail", args=(self.pk,))
