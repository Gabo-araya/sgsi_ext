from io import BytesIO
from unittest.mock import patch

import requests

from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers

from base.tests import BaseTestCase

from ..models import ClientLog
from ..services.client import ApiClientConfiguration
from ..services.client import JsonApiClient


class JsonApiClientTests(BaseTestCase):
    databases = ["default", "logs"]

    def _setup_mock_response(self, mock_obj, status_code, content_type=None, body=None):
        mock_response = requests.Response()
        mock_response.status_code = status_code
        mock_response.headers = CaseInsensitiveDict({"Content-Type": content_type})
        mock_response.encoding = get_encoding_from_headers(mock_response.headers)
        mock_response.raw = BytesIO(body)

        mock_obj.return_value = mock_response

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.patcher = patch(
            "api_client.services.client.JsonApiClient.validate_configuration"
        )
        cls.patcher.start()

        config = ApiClientConfiguration(
            scheme="http", host="example.com", code="json_test"
        )
        cls.api_client = JsonApiClient(config)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.patcher.stop()

    @patch("requests.Session.send")
    def test_request_returning_404_with_json_body_returns_content(self, patched_send):
        """Request with a 404 response with body should return content"""
        self._setup_mock_response(
            patched_send,
            404,
            "application/json",
            b"""{"message": "Not found"}""",
        )

        (response, code), error = self.api_client.get_blocking("/test/")
        self.assertEqual({"message": "Not found"}, response)
        self.assertEqual(404, code)

    @patch("requests.Session.send")
    def test_request_returning_404_with_declared_html_body_returns_error(
        self, patched_send
    ):
        """Request with 404 response with body with content-type should return error"""
        self._setup_mock_response(
            patched_send,
            404,
            "text/html",
            b"""<html><body><p>Not found</p></body></html>""",
        )

        (response, code), error = self.api_client.get_blocking("/test/")
        self.assertIs(type(error), requests.RequestException)
        self.assertIsNone(code)
        self.assertTrue(ClientLog.objects.exists())

    @patch("requests.Session.send")
    def test_request_returning_404_with_undeclared_html_body_returns_error(
        self, patched_send
    ):
        """Request with 404 response with body w/o content-type should return error"""
        self._setup_mock_response(
            patched_send,
            404,
            None,
            b"""<html><body><p>Not found</p></body></html>""",
        )

        (response, code), error = self.api_client.get_blocking("/test/")
        self.assertIs(type(error), requests.JSONDecodeError)
        self.assertIsNone(code)
        self.assertTrue(ClientLog.objects.exists())

    @patch("requests.Session.send")
    def test_request_returning_404_without_body_returns_none(self, patched_send):
        """Request with a 404 response with body should return None"""
        self._setup_mock_response(patched_send, 404, "application/json")

        (response, code), error = self.api_client.get_blocking("/test/")
        self.assertEqual(None, response)
        self.assertEqual(404, code)

    @patch("requests.Session.send")
    def test_request_returning_malformed_json_body_returns_error(self, patched_send):
        """Request with malformed JSON response should return error"""
        self._setup_mock_response(
            patched_send,
            200,
            "application/json",
            b"""{malformed: "body"}""",
        )

        (response, code), error = self.api_client.get_blocking("/test/")
        self.assertIs(type(error), requests.JSONDecodeError)
        self.assertIsNone(code)
        self.assertTrue(ClientLog.objects.exists())
