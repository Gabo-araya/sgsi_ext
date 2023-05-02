import os

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)
from django.utils.autoreload import DJANGO_AUTORELOAD_ENV

from ..print_to_dos import print_to_dos


def is_first_run():
    return os.environ.get(DJANGO_AUTORELOAD_ENV) != "true"


class Command(RunserverCommand):
    def handle(self, *args, **options):
        if settings.DEBUG and is_first_run():
            print_to_dos()
        return super().handle(*args, **options)
