from unittest.mock import patch

import pytest

from ..services.client.errors import DisabledClientError

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
    assert isinstance(error, DisabledClientError)
