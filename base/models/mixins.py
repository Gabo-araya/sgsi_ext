import hashlib

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.fields.base import BaseFileField


class FileIntegrityModelBase(models.Model):
    """
    Base model for models that have a file field and need to have a shasum field.
    """

    file = BaseFileField(verbose_name=_("file"))
    shasum = models.CharField(verbose_name=_("shasum"), max_length=64)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        self._set_shasum_of_file()
        return super().save(*args, **kwargs)

    def _set_shasum_of_file(self) -> str:
        self.shasum = self.get_shasum_of_file()

    def get_shasum_of_file(self) -> str:
        sha256 = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()
