import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

EXCLUDED_APPS = set()


class Command(BaseCommand):
    help = (  # noqa: A003
        "Checks that no installed app"
        " is missing from the hardcoded TARGET_APPS to translate."
    )

    def add_arguments(self, parser):
        parser.add_argument("target_app", nargs="+")

    def handle(self, *args, **options):
        installed_apps = set(settings.INSTALLED_APPS)
        existing_dirs = {d.name for d in os.scandir(settings.BASE_DIR) if d.is_dir()}
        target_apps = set(options["target_app"])
        missing_apps = (installed_apps & existing_dirs) - target_apps - EXCLUDED_APPS

        if len(missing_apps) > 0:
            self.stderr.write(
                "Error: the following apps"
                " should be included in `TARGET_APPS` for translation,"
                f" or excluded in `EXCLUDED_APPS`:\n{missing_apps}"
            )
            sys.exit(1)
