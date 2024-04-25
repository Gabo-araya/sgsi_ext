from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.versionable_mixin import VersionableMixin


class Process(VersionableMixin, BaseModel):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("process")
        verbose_name_plural = _("processes")

    @property
    def can_add_new_versions(self) -> bool:
        return not self.versions.not_published().exists()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("process_detail", args=(self.pk,))
