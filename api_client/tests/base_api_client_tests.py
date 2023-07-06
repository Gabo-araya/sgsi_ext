import pytest

from api_client.enums import ClientCodes
from api_client.services.client.api_client import ApiClient
from api_client.services.client.config import ApiClientConfiguration
from api_client.services.client.errors import ClientConfigurationError


def test_validate_configuration_raises_on_wrong_code():
    with pytest.raises(ClientConfigurationError):
        config = ApiClientConfiguration(
            scheme="http", host="example.com/", code="non-existing-code"
        )
        ApiClient(config)


def test_validate_configuration_raises_on_wrong_timeout(settings):
    settings.API_CLIENT_MAX_TIMEOUT = 0
    with pytest.raises(ClientConfigurationError):
        config = ApiClientConfiguration(
            scheme="http",
            host="example.com/",
            code=ClientCodes.DUMMY_INTEGRATION,
            timeout=1,
        )
        ApiClient(config)
