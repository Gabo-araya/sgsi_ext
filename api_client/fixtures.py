from datetime import timedelta

import pytest

from api_client.enums import ClientCodes
from api_client.models import ClientConfig
from api_client.models import ClientLog
from base import utils


@pytest.fixture
def client_config(db) -> ClientConfig:
    return ClientConfig.objects.create(client_code=ClientCodes.DUMMY_INTEGRATION)


@pytest.fixture
def client_log(db) -> ClientLog:
    return ClientLog.objects.create(client_code=ClientCodes.DUMMY_INTEGRATION)


@pytest.fixture
def client_logs(db) -> list[ClientLog]:
    today = utils.today()
    yesterday = utils.today() - timedelta(days=1)
    log_1 = ClientLog.objects.create(client_code=ClientCodes.DUMMY_INTEGRATION)
    log_1.created_at = today
    log_1.save()
    log_2 = ClientLog.objects.create(client_code=ClientCodes.DUMMY_INTEGRATION)
    log_2.created_at = yesterday
    log_2.save()

    return [log_1, log_2]
