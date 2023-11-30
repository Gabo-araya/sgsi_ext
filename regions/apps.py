from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RegionsConfig(AppConfig):
    verbose_name = _("regions")
    name = "regions"
