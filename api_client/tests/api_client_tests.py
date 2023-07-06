from unittest.mock import patch

import pytest

from api_client.services.client import config
from api_client.services.client import errors
from api_client.services.client.auth import BasicAuth

PARAMETRIZED_GET_URL_TESTS = {
    "empty": ("", None, "http://example.com/"),
    "nonempty": ("test", None, "http://example.com/test"),
    "nonempty-with-parameters": ("test/{pk}", {"pk": "5"}, "http://example.com/test/5"),
    "empty-trailing-slash": ("/", None, "http://example.com/"),
    "nonempty-leading-slash": ("/test", None, "http://example.com/test"),
    "nonempty-with-parameters-leading-slash": (
        "/test/{pk}",
        {"pk": "5"},
        "http://example.com/test/5",
    ),
    "nonempty-trailing-slash": ("test/", None, "http://example.com/test/"),
    "nonempty-with-parameters-trailing-slash": (
        "test/{pk}/",
        {"pk": "5"},
        "http://example.com/test/5/",
    ),
    "nonempty-leading-trailing-slash": ("/test/", None, "http://example.com/test/"),
    "nonempty-with-parameters-leading-trailing-slash": (
        "/test/{pk}/",
        {"pk": "5"},
        "http://example.com/test/5/",
    ),
}


@pytest.mark.parametrize(
    ("raw_url", "parameters", "expected_url"),
    PARAMETRIZED_GET_URL_TESTS.values(),
    ids=PARAMETRIZED_GET_URL_TESTS.keys(),
)
def test_get_url(test_apiclient, raw_url, parameters, expected_url):
    if parameters is None:
        assert test_apiclient.get_url(raw_url) == expected_url

    assert test_apiclient.get_url(raw_url, parameters) == expected_url


@pytest.mark.parametrize(
    ("raw_url", "parameters", "expected_url"),
    PARAMETRIZED_GET_URL_TESTS.values(),
    ids=PARAMETRIZED_GET_URL_TESTS.keys(),
)
def test_get_url_host_trailing_slash(
    test_apiclient_with_trailing_slash, raw_url, parameters, expected_url
):
    if parameters is None:
        assert test_apiclient_with_trailing_slash.get_url(raw_url) == expected_url

    assert (
        test_apiclient_with_trailing_slash.get_url(raw_url, parameters) == expected_url
    )


@pytest.mark.parametrize(
    ("parameters", "expected_url"),
    (
        ({"category": "test", "pk": "5"}, "http://example.com/test/5/"),
        ({"category": 1, "pk": 5}, "http://example.com/1/5/"),
        ({"category": "test", "pk": 5}, "http://example.com/test/5/"),
    ),
    ids=("only-str", "only-int", "mixed"),
)
def test_get_url_with_path_params(test_apiclient, parameters, expected_url):
    assert test_apiclient.get_url("{category}/{pk}/", parameters) == expected_url


def test_making_request_to_disabled_client_should_return_error(
    disabled_apiclient, setup_mock_response
):
    with patch("requests.Session.send") as mock_send:
        setup_mock_response(mock_send, 200, "application/json", b"""OK""")
        response, error = disabled_apiclient.get_blocking("/test")

    assert response == disabled_apiclient.empty_response
    assert isinstance(error, errors.DisabledClientError)


def test_serialize_configuration():
    with patch("api_client.services.client.ApiClient.validate_configuration"):
        auth = BasicAuth("magnet", "verysecretpleasedontsteal")
        config_obj = config.ApiClientConfiguration(
            scheme="http", host="example.com", code="test", auth=auth
        )

    expected_serialization = {
        "host": "example.com",
        "code": "test",
        "scheme": "http",
        "timeout": config.DEFAULT_TIMEOUT,
        "auth_class": "api_client.services.client.auth.BasicAuth",
        "auth_class_config": {
            "username": "magnet",
            "password": "verysecretpleasedontsteal",
        },
    }
    assert config_obj.serialize() == expected_serialization


def test_deserialize_configuration():
    serialized_config = {
        "code": "test",
        "scheme": "http",
        "host": "example.com",
        "timeout": config.DEFAULT_TIMEOUT,
        "auth_class": "api_client.services.client.auth.BasicAuth",
        "auth_class_config": {
            "username": "magnet",
            "password": "verysecretpleasedontsteal",
        },
    }

    with patch("api_client.services.client.ApiClient.validate_configuration"):
        config_obj = config.ApiClientConfiguration.from_serialized_configuration(
            **serialized_config
        )

    assert config_obj.code == "test"
    assert config_obj.scheme == "http"
    assert config_obj.host == "example.com"
    assert config_obj.timeout == config.DEFAULT_TIMEOUT
    assert isinstance(config_obj.auth, BasicAuth)
    assert config_obj.auth.username == "magnet"
    assert config_obj.auth.password == "verysecretpleasedontsteal"  # noqa: S105
