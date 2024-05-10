from django.conf import settings
from django.contrib.auth import models as auth_models

from typing_extensions import Self


class Group(auth_models.Group):
    class Meta:
        proxy = True

    @classmethod
    def get_default_group_name(cls) -> str:
        return settings.DEFAULT_GROUP_NAME

    @classmethod
    def get_default_group(cls) -> Self | None:
        if not (default_group_name := cls.get_default_group_name()):
            return None
        return cls.objects.get_or_create(name=default_group_name)[0]

    @classmethod
    def get_default_group_queryset(cls):
        return cls.objects.filter(name=cls.get_default_group_name())
