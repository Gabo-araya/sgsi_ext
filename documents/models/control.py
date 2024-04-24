from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from documents.models.control_category import ControlCategory
from documents.models.document import Document


class Control(BaseModel):
    category = models.ForeignKey(
        verbose_name=_("category"),
        to=ControlCategory,
        on_delete=models.PROTECT,
        related_name="controls",
        null=True,
        blank=True,
    )
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
    )
    document = models.ForeignKey(
        verbose_name=_("document"),
        to=Document,
        on_delete=models.PROTECT,
        related_name="controls",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("control")
        verbose_name_plural = _("controls")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("control_detail", args=(self.pk,))
