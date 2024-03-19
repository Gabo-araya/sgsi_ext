from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class DocumentReadByUser(BaseModel):
    document_version = models.ForeignKey(
        "documents.DocumentVersion",
        verbose_name=_("document version"),
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("document read by user")
        verbose_name_plural = _("documents read by users")
