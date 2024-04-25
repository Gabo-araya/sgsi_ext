from django.db import models


class IncrementFieldModelBase(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding:
            self._auto_increment_field(self._get_field_to_increment())
        super().save(*args, **kwargs)

    def _auto_increment_field(self, field: str) -> None:
        last = (
            self._get_increment_queryset()
            .aggregate(models.Max(field))
            .get(f"{field}__max")
        )
        setattr(self, field, last + 1 if last is not None else 1)

    def _get_increment_queryset(self) -> type[models.QuerySet]:
        msg = f"You must define {self.__class__.__name__}._get_increment_queryset()"
        raise NotImplementedError(msg)

    def _get_field_to_increment(self) -> str:
        msg = f"You must define {self.__class__.__name__}._get_field_to_increment()"
        raise NotImplementedError(msg)
