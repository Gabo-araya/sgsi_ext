# django
from django.conf import settings

# others libraries
from django_extensions.management.commands.runserver_plus import (
    Command as RunserverCommand,
)

from ..print_TODOs import print_TODOs


def is_first_run():
    try:
        # others libraries
        from werkzeug.serving import is_running_from_reloader
    except ImportError:
        # super() will print an error later.
        return True

    return not is_running_from_reloader()


class Command(RunserverCommand):
    def handle(self, *args, **options):
        if settings.DEBUG and not is_first_run():
            print_TODOs()
        return super().handle(*args, **options)
