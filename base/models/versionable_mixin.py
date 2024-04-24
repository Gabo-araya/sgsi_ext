import datetime

from typing import Any

from django.db import models

from users.models import User


class VersionableMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if not hasattr(self, "versions"):
            msg = f"{self.__class__.__name__} must have a 'versions' relation"
            raise AttributeError(msg)

    @property
    def last_version(self) -> type[models.Model] | None:
        return self.versions.order_by("-version").first()

    @property
    def latest_update(self) -> datetime.datetime:
        if not self.versions.exists():
            return self.updated_at
        return max(self.updated_at, self.versions.latest("updated_at").updated_at)

    @property
    def latest_updator(self) -> User:
        if not self.versions.exists():
            return self.updated_by
        return max(
            self, self.versions.latest("updated_at"), key=lambda x: x.updated_at
        ).updated_by
