from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiClientConfig(AppConfig):
    name = "api_client"
    verbose_name = _("api_client")

    def ready(self) -> None:
        from . import signals  # noqa: F401

        return super().ready()
