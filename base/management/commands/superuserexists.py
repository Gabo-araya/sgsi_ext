import sys

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Returns 0 only if there's an active superuser account"  # noqa: A003

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True, is_active=True)
        sys.exit(0 if superusers.exists() else 1)
