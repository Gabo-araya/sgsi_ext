from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "base"

    def ready(self) -> None:
        from . import signals  # noqa: F401

        return super().ready()
