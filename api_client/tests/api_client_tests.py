from api_client.services.clients import ApiClientConfiguration
from api_client.services.clients.api_client import ApiClient
from base.tests import BaseTestCase


class ApiClientGetUrlTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        config = ApiClientConfiguration(scheme="http", host="example.com", code="test")
        cls.api_client = ApiClient(config)

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
        config = ApiClientConfiguration(scheme="http", host="example.com", code="test")
        cls.api_client = ApiClient(config)

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
