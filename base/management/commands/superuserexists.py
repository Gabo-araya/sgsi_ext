import sys

from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Returns 0 only if there's an active superuser account"

    def handle(self, *args, **options):
        exists = User.objects.filter(is_superuser=True, is_active=True)
        sys.exit(0 if exists else 1)
