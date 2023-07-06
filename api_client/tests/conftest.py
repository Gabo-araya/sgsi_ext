from datetime import timedelta
from io import BytesIO
from unittest.mock import patch

import pytest
import requests

from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers

from api_client.enums import ClientCodes
from api_client.models import ClientConfig
from api_client.models import ClientLog
from api_client.services.client import ApiClient
from api_client.services.client import ApiClientConfiguration
from api_client.services.client import JsonApiClient
from base import utils


@pytest.fixture
def client_log_queryset(db):
    today = utils.today()
    yesterday = utils.today() - timedelta(days=1)
    log_1 = ClientLog.objects.create()
    log_1.created_at = today
    log_1.save()
    log_2 = ClientLog.objects.create()
    log_2.created_at = yesterday
    log_2.save()
    return ClientLog.objects.all()


@pytest.fixture
def client_config(db) -> ClientConfig:
    return ClientConfig.objects.create(client_code=ClientCodes.DUMMY_INTEGRATION)


@pytest.fixture
def test_apiclient() -> ApiClient:
    with patch("api_client.services.client.ApiClient.validate_configuration"):
        config = ApiClientConfiguration(
            scheme="http", host="example.com", code=ClientCodes.DUMMY_INTEGRATION
        )
        return ApiClient(config)


@pytest.fixture
def test_apiclient_with_trailing_slash() -> ApiClient:
    with patch("api_client.services.client.ApiClient.validate_configuration"):
        config = ApiClientConfiguration(
            scheme="http", host="example.com/", code=ClientCodes.DUMMY_INTEGRATION
        )
        return ApiClient(config)


@pytest.fixture
def disabled_apiclient(test_apiclient, db) -> ApiClient:
    ClientConfig.objects.create(
        client_code=ClientCodes.DUMMY_INTEGRATION, enabled=False
    )
    return test_apiclient


@pytest.fixture
def test_json_apiclient() -> ApiClient:
    with patch("api_client.services.client.JsonApiClient.validate_configuration"):
        config = ApiClientConfiguration(
            scheme="http", host="example.com", code="json_test"
        )
        return JsonApiClient(config)


@pytest.fixture
def setup_mock_response():
    def _setup_mock_response(mock_obj, status_code, content_type=None, body=None):
        mock_response = requests.Response()
        mock_response.status_code = status_code
        mock_response.headers = CaseInsensitiveDict({"Content-Type": content_type})
        mock_response.encoding = get_encoding_from_headers(mock_response.headers)
        mock_response.raw = BytesIO(body)

        mock_obj.return_value = mock_response

    return _setup_mock_response
