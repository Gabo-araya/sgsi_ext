# others libraries
from django.conf import settings

from django_extensions.management.commands.runserver_plus import (
    Command as RunserverCommand,
)

from ..print_to_dos import print_to_dos


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
        if settings.DEBUG and is_first_run():
            print_to_dos()
        return super().handle(*args, **options)
