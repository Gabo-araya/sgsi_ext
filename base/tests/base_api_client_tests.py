from base.services import BaseApiClient
from base.services.base_api_client.base_api_client import BaseConfiguration
from base.tests import BaseTestCase


class MockApiClient(BaseApiClient):
    def __init__(self, mock_host: str) -> None:
        self.mock_host = mock_host
        super().__init__()

    def get_configuration(self) -> BaseConfiguration:
        return {
            "host": self.mock_host,
            "protocol": "http",
            "timeout": 10,
        }


class BaseApiClientGetUrlTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_get_url_without_end_slashes(self):
        client = MockApiClient("example.com")
        self.assertEqual(client.get_url(""), "http://example.com/")
        self.assertEqual(client.get_url("test"), "http://example.com/test")
        self.assertEqual(
            client.get_url("test/{pk}", {"pk": "5"}), "http://example.com/test/5"
        )

    def test_get_url_with_end_slashes(self):
        client = MockApiClient("example.com/")
        self.assertEqual(client.get_url("/"), "http://example.com/")
        self.assertEqual(client.get_url("test/"), "http://example.com/test/")
        self.assertEqual(
            client.get_url("test/{pk}/", {"pk": "5"}), "http://example.com/test/5/"
        )

    def test_get_url_with_base_url_end_slash_and_without_endpoint_end_slash(self):
        client = MockApiClient("example.com/")
        self.assertEqual(client.get_url(""), "http://example.com/")
        self.assertEqual(client.get_url("test"), "http://example.com/test")
        self.assertEqual(
            client.get_url("test/{pk}", {"pk": "5"}), "http://example.com/test/5"
        )

    def test_get_url_without_base_url_end_slash_and_with_endpoint_end_slash(self):
        client = MockApiClient("example.com")
        self.assertEqual(client.get_url("/"), "http://example.com/")
        self.assertEqual(client.get_url("test/"), "http://example.com/test/")
        self.assertEqual(
            client.get_url("test/{pk}/", {"pk": "5"}), "http://example.com/test/5/"
        )
