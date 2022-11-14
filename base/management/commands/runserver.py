# standard library
import os

# django
from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)
from django.utils.autoreload import DJANGO_AUTORELOAD_ENV

from ..print_TODOs import print_TODOs


def is_running_from_reloader():
    return os.environ.get(DJANGO_AUTORELOAD_ENV) == "true"


class Command(RunserverCommand):
    def handle(self, *args, **options):
        if settings.DEBUG and not is_running_from_reloader():
            print_TODOs()
        return super().handle(*args, **options)
