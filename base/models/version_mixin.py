from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.increment_field_mixin import IncrementFieldModelBase


class VersionModelBase(IncrementFieldModelBase, models.Model):
    version = models.PositiveSmallIntegerField(
        verbose_name=_("version"),
    )

    class Meta:
        abstract = True

    def _get_field_to_increment(self) -> str:
        return "version"
