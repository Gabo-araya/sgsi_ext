from base.services import BaseApiClient
from base.tests import BaseTestCase


class MockApiClient(BaseApiClient):
    def __init__(self, mock_host: str) -> None:
        self.mock_host = mock_host
        super().__init__()

    def get_extra_configuration(self):
        return {
            "host": self.mock_host,
            "schema": "http",
        }


class BaseApiClientGetUrlTestCase(BaseTestCase):
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


class BaseApiClientPathParamsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_api_client = MockApiClient("example.com")

    def test_only_str_path_params(self):
        self.assertEqual(
            self.mock_api_client.get_url(
                "{category}/{pk}/",
                {"category": "test", "pk": "5"},
            ),
            "http://example.com/test/5/",
        )

    def test_only_int_path_params(self):
        self.assertEqual(
            self.mock_api_client.get_url(
                "{category}/{pk}/",
                {"category": 1, "pk": 5},
            ),
            "http://example.com/1/5/",
        )

    def test_mixed_path_params(self):
        self.assertEqual(
            self.mock_api_client.get_url(
                "{category}/{pk}/",
                {"category": "test", "pk": 5},
            ),
            "http://example.com/test/5/",
        )
