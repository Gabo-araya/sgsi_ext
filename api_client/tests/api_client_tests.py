from io import BytesIO
from unittest.mock import patch

import requests

from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers

from base.tests import BaseTestCase

from ..models import DisabledClient
from ..services.client import ApiClient
from ..services.client import ApiClientConfiguration
from ..services.client.errors import DisabledClientError


class ApiClientGetUrlTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.patcher = patch(
            "api_client.services.client.ApiClient.validate_configuration"
        )
        cls.patcher.start()

        config = ApiClientConfiguration(scheme="http", host="example.com", code="test")
        cls.api_client = ApiClient(config)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.patcher.stop()

    def test_get_url_without_end_slashes(self):
        self.assertEqual(self.api_client.get_url(""), "http://example.com/")
        self.assertEqual(self.api_client.get_url("test"), "http://example.com/test")
        self.assertEqual(
            self.api_client.get_url("test/{pk}", {"pk": "5"}),
            "http://example.com/test/5",
        )

    def test_get_url_with_end_slashes(self):
        self.assertEqual(self.api_client.get_url("/"), "http://example.com/")
        self.assertEqual(self.api_client.get_url("test/"), "http://example.com/test/")
        self.assertEqual(
            self.api_client.get_url("test/{pk}/", {"pk": "5"}),
            "http://example.com/test/5/",
        )

    def test_get_url_with_base_url_end_slash_and_without_endpoint_end_slash(self):
        self.assertEqual(self.api_client.get_url(""), "http://example.com/")
        self.assertEqual(self.api_client.get_url("test"), "http://example.com/test")
        self.assertEqual(
            self.api_client.get_url("test/{pk}", {"pk": "5"}),
            "http://example.com/test/5",
        )

    def test_get_url_without_base_url_end_slash_and_with_endpoint_end_slash(self):
        self.assertEqual(self.api_client.get_url("/"), "http://example.com/")
        self.assertEqual(self.api_client.get_url("test/"), "http://example.com/test/")
        self.assertEqual(
            self.api_client.get_url("test/{pk}/", {"pk": "5"}),
            "http://example.com/test/5/",
        )


class ApiClientPathParamsTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.patcher = patch(
            "api_client.services.client.ApiClient.validate_configuration"
        )
        cls.patcher.start()
        config = ApiClientConfiguration(scheme="http", host="example.com", code="test")
        cls.api_client = ApiClient(config)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.patcher.stop()

    def test_only_str_path_params(self):
        self.assertEqual(
            self.api_client.get_url(
                "{category}/{pk}/",
                {"category": "test", "pk": "5"},
            ),
            "http://example.com/test/5/",
        )

    def test_only_int_path_params(self):
        self.assertEqual(
            self.api_client.get_url(
                "{category}/{pk}/",
                {"category": 1, "pk": 5},
            ),
            "http://example.com/1/5/",
        )

    def test_mixed_path_params(self):
        self.assertEqual(
            self.api_client.get_url(
                "{category}/{pk}/",
                {"category": "test", "pk": 5},
            ),
            "http://example.com/test/5/",
        )


class DisabledApiClientTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.patcher = patch(
            "api_client.services.client.ApiClient.validate_configuration"
        )
        cls.patcher.start()
        config = ApiClientConfiguration(scheme="http", host="example.com", code="test")
        cls.api_client = ApiClient(config)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.patcher.stop()

    def _setup_mock_response(self, mock_obj, status_code, content_type=None, body=None):
        mock_response = requests.Response()
        mock_response.status_code = status_code
        mock_response.headers = CaseInsensitiveDict({"Content-Type": content_type})
        mock_response.encoding = get_encoding_from_headers(mock_response.headers)
        mock_response.raw = BytesIO(body)

        mock_obj.return_value = mock_response

    def test_making_request_to_disabled_client_should_raise(self):
        """Make a request with a disabled client should raise an exception."""
        DisabledClient.objects.create(client_code="test")

        with patch("requests.Session.send") as mock_send:
            self._setup_mock_response(mock_send, 200, "application/json", b"""OK""")
            response, error = self.api_client.get_blocking("/test")

        self.assertEqual(response, self.api_client.empty_response)
        self.assertIsInstance(error, DisabledClientError)
