from unittest.mock import patch

import pytest
import requests

from ..models import ClientLog


@pytest.mark.django_db(databases=["default", "logs"])
def test_request_returning_404_with_json_body_returns_content(
    test_json_apiclient,
    setup_mock_response,
):
    with patch("requests.Session.send") as mock_send:
        setup_mock_response(
            mock_send, 404, "application/json", b"""{"message": "Not found"}"""
        )
        (response, code), error = test_json_apiclient.get_blocking("/test")

    assert response == {"message": "Not found"}
    assert code == 404


@pytest.mark.django_db(databases=["default", "logs"])
def test_request_returning_404_with_declared_html_body_returns_error(
    test_json_apiclient,
    setup_mock_response,
):
    with patch("requests.Session.send") as mock_send:
        setup_mock_response(
            mock_send,
            404,
            "application/json",
            b"""<html><body><p>Not found</p></body></html>""",
        )
        (response, code), error = test_json_apiclient.get_blocking("/test")

    assert response is None
    assert code is None
    assert isinstance(error, requests.RequestException)
    assert ClientLog.objects.exists()


@pytest.mark.django_db(databases=["default", "logs"])
def test_request_returning_404_with_undeclared_html_body_returns_error(
    test_json_apiclient,
    setup_mock_response,
):
    with patch("requests.Session.send") as mock_send:
        setup_mock_response(
            mock_send,
            404,
            None,
            b"""<html><body><p>Not found</p></body></html>""",
        )
        (response, code), error = test_json_apiclient.get_blocking("/test")

    assert response is None
    assert code is None
    assert isinstance(error, requests.JSONDecodeError)
    assert ClientLog.objects.exists()


@pytest.mark.django_db(databases=["default", "logs"])
def test_request_returning_404_without_body_returns_none(
    test_json_apiclient,
    setup_mock_response,
):
    with patch("requests.Session.send") as mock_send:
        setup_mock_response(mock_send, 404, "application/json")
        (response, code), error = test_json_apiclient.get_blocking("/test")

    assert response is None
    assert code == 404


@pytest.mark.django_db(databases=["default", "logs"])
def test_request_returning_malformed_json_body_returns_error(
    test_json_apiclient,
    setup_mock_response,
):
    with patch("requests.Session.send") as mock_send:
        setup_mock_response(
            mock_send,
            200,
            "application/json",
            b"""{malformed: "body"}""",
        )
        (response, code), error = test_json_apiclient.get_blocking("/test")

    assert response is None
    assert code is None
    assert isinstance(error, requests.JSONDecodeError)
    assert ClientLog.objects.exists()
