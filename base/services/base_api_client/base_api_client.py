import os

from abc import ABC
from abc import abstractmethod
from urllib.parse import quote

import requests

DEFAULT_TIMEOUT = 10
DEFAULT_PROTCOL = "https"


class BaseApiClient(ABC):
    def __init__(self) -> None:
        self.configuration = self.get_configuration()

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.get(
            url,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def post_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, str] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.post(
            url,
            json=body,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def patch_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, str] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.patch(
            url,
            json=body,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def put_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, str] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.put(
            url,
            json=body,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.delete(
            url,
            timeout=self.configuration["timeout"],
        )

    def get_url(
        self, endpoint: str, path_params: dict[str, str | int] | None = None
    ) -> str:
        parsed_endpoint = self.parse_endpoint(endpoint, path_params)
        return os.path.join(self.base_url, parsed_endpoint)

    def parse_endpoint(
        self, endpoint: str, path_params: dict[str, str | int] | None = None
    ) -> str:
        parsed_endpoint = endpoint.lstrip("/")
        parsed_path_params = self.parse_path_params(path_params)
        if parsed_path_params:
            return parsed_endpoint.format(**parsed_path_params)
        return parsed_endpoint

    @staticmethod
    def parse_path_params(
        path_params: dict[str, str | int] | None = None
    ) -> dict | None:
        if not path_params:
            return None
        return {
            key: quote(str(value), safe="")
            for key, value in path_params.items()
            if value is not None
        }

    @property
    def base_url(self) -> str:
        protocol = self.configuration["protocol"]
        host = self.configuration["host"]
        return f"{protocol}://{host.strip('/')}"

    def get_configuration(self) -> dict:
        return {
            **self.get_default_configuration(),
            **self.get_extra_configuration(),
        }

    def get_default_configuration(self):
        return {
            "timeout": DEFAULT_TIMEOUT,
            "protocol": DEFAULT_PROTCOL,
        }

    @abstractmethod
    def get_extra_configuration(self) -> dict:
        ...
