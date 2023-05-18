from django.db import models
from django.utils import timezone


class ClientLogQueryset(models.QuerySet):
    def old(self):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        return self.filter(created_at__lt=one_year_ago)
