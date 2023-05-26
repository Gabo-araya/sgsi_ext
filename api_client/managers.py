from django.db import models
from django.utils import timezone

from api_client.enums import ClientCodes


class ClientLogQueryset(models.QuerySet):
    def old(self):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        return self.filter(created_at__lt=one_year_ago)


class DisabledClientQueryset(models.QuerySet):
    def is_disabled(self, client_code: ClientCodes):
        return self.filter(client_code=client_code).exists()
