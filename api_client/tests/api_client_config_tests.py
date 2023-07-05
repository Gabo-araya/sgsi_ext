import pytest


@pytest.mark.django_db(databases=["default"])
def test_api_client_config_str_should_include_client_code(client_config):
    assert client_config.client_code in str(client_config)
