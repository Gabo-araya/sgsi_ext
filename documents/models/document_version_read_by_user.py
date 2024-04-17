from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class DocumentVersionReadByUser(BaseModel):
    document_version = models.ForeignKey(
        "documents.DocumentVersion",
        verbose_name=_("document version"),
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("document version read by user")
        verbose_name_plural = _("document versions read by users")
        constraints = (
            models.UniqueConstraint(
                fields=("document_version", "user"),
                name="unique_document_version_read_by_user",
            ),
        )
