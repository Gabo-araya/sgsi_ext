import pytest

from api_client.models import ClientLog
from api_client.tasks import client_log_cleanup


@pytest.mark.django_db(databases=["default", "logs"])
def test_client_log_cleanup(client_log, settings):
    settings.API_CLIENT_LOG_MAX_AGE_DAYS = 0
    assert ClientLog.objects.count() == 1
    client_log_cleanup()
    assert ClientLog.objects.count() == 0
