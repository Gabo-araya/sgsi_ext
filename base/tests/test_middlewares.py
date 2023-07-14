from unittest.mock import MagicMock
from unittest.mock import PropertyMock
from unittest.mock import patch

from django.http import HttpResponse
from django.http import HttpResponseServerError

import pytest

from base.middleware import ReadinessCheckMiddleware


@pytest.mark.parametrize(
    ("method", "path", "expected_check_calls", "expected_get_response_calls"),
    (
        ("GET", "/_ready/", 1, 0),
        ("POST", "/_ready/", 0, 1),
        ("PUT", "/_ready/", 0, 1),
        ("OPTIONS", "/_ready/", 0, 1),
        ("HEAD", "/_ready/", 0, 1),
        ("PATCH", "/_ready/", 0, 1),
        ("DELETE", "/_ready/", 0, 1),
        ("GET", "/other/", 0, 1),
        ("POST", "/other/", 0, 1),
        ("PUT", "/other/", 0, 1),
        ("OPTIONS", "/other/", 0, 1),
        ("HEAD", "/other/", 0, 1),
        ("PATCH", "/other/", 0, 1),
        ("DELETE", "/other/", 0, 1),
    ),
)
def test_readiness_check_middleware_process_request(
    method, path, expected_check_calls, expected_get_response_calls, rf
):
    with (
        patch(
            "base.middleware.ReadinessCheckMiddleware.perform_readiness_check"
        ) as perform_readiness_check_mock,
    ):
        request = rf.generic(method, path)
        middleware = ReadinessCheckMiddleware(MagicMock())
        middleware.process_request(request)
        assert perform_readiness_check_mock.call_count == expected_check_calls
        assert middleware.get_response.call_count == expected_get_response_calls


@pytest.mark.parametrize(
    ("side_effect", "expected_class_type"),
    (
        (None, str),
        (Exception, HttpResponseServerError),
    ),
)
def test_readiness_check_middleware_perform_readiness_request(
    side_effect, expected_class_type
):
    with (
        patch(
            "base.middleware.ReadinessCheckMiddleware.check_connections",
            side_effect=side_effect,
            return_value="check_connections_return_value",
        )
    ):
        middleware = ReadinessCheckMiddleware(MagicMock())
        assert isinstance(middleware.perform_readiness_check(), expected_class_type)


@pytest.mark.parametrize(
    ("fetchone_return_value", "expected_check"),
    ((None, HttpResponseServerError), ("fetchone_return_value", HttpResponse)),
)
def test_readiness_check_middleware_check_connections(
    fetchone_return_value, expected_check
):
    mock = MagicMock()
    mock.cursor.fetchone.return_value = fetchone_return_value
    mock.cursor.return_value = mock.cursor
    with patch(
        "django.db.connections",
        new_callable=PropertyMock(
            return_value={
                "default": mock,
            }
        ),
    ):
        middleware = ReadinessCheckMiddleware(MagicMock())
        assert isinstance(middleware.check_connections(), expected_check)
