from django.db import models
from django.utils.translation import gettext_lazy as _


class VersionModelBase(models.Model):
    version = models.PositiveSmallIntegerField(
        verbose_name=_("version"),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding:
            self._auto_increment_version()
        super().save(*args, **kwargs)

    def _auto_increment_version(self) -> None:
        last_version = (
            self._get_versioned_instance()
            .versions.aggregate(models.Max("version"))
            .get("version__max")
        )
        self.version = last_version + 1 if last_version is not None else 1

    def _get_versioned_instance(self) -> type[models.Model]:
        msg = f"you must define {self.__class__.__name__}._get_versioned_instance()"
        raise NotImplementedError(msg)
