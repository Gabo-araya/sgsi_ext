from django.conf import settings
from django.db import models
from django.utils import timezone

from api_client.enums import ClientCodes


class ClientLogQueryset(models.QuerySet):
    def old(self):
        days = settings.API_CLIENT_LOG_MAX_AGE_DAYS
        deletion_time = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__lt=deletion_time)


class ClientConfigQueryset(models.QuerySet):
    def is_disabled(self, client_code: ClientCodes):
        client_config, _ = self.get_or_create(client_code=client_code)
        return not client_config.enabled

    def get_total_retries(self, client_code: ClientCodes):
        client_config, _ = self.get_or_create(client_code=client_code)
        return client_config.retries
