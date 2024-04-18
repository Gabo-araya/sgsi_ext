from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class DocumentVersionReadByUser(BaseModel):
    document_version = models.ForeignKey(
        verbose_name=_("document version"),
        to="documents.DocumentVersion",
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("document version read by user")
        verbose_name_plural = _("document versions read by users")
        constraints = (
            models.UniqueConstraint(
                fields=("document_version", "user"),
                name="unique_document_version_read_by_user",
            ),
        )
