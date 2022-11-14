# django
from django.conf import settings

# others libraries
from django_extensions.management.commands.runserver_plus import (
    Command as RunserverCommand,
)
from werkzeug.serving import is_running_from_reloader

from ..print_TODOs import print_TODOs


class Command(RunserverCommand):
    def handle(self, *args, **options):
        if settings.DEBUG and not is_running_from_reloader():
            print_TODOs()
        return super().handle(*args, **options)
