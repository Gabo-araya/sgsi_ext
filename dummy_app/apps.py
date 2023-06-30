from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DummyAppConfig(AppConfig):
    name = "dummy_app"
    verbose_name = _("dummy_app")
