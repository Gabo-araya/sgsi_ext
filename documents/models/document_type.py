from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel


class DocumentType(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _("document type")
        verbose_name_plural = _("document types")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("documenttype_detail", args=(self.pk,))
