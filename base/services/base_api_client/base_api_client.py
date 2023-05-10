import os

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import TypedDict
from urllib.parse import quote

import requests


class BaseConfiguration(TypedDict):
    timeout: int
    protocol: str
    host: str


class BaseApiClient(ABC):
    def __init__(self) -> None:
        self.configuration = self.get_configuration()

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
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
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
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
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
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
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
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
        path_params: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.delete(
            url,
            timeout=self.configuration["timeout"],
        )

    def get_url(self, endpoint: str, path_params: dict | None = None) -> str:
        parsed_endpoint = self.parse_endpoint(endpoint, path_params)
        return os.path.join(self.base_url, parsed_endpoint)

    def parse_endpoint(self, endpoint: str, path_params: dict | None = None) -> str:
        parsed_endpoint = endpoint.lstrip("/")
        parsed_path_params = self.parse_path_params(path_params)
        if parsed_path_params:
            return parsed_endpoint.format(**parsed_path_params)
        return parsed_endpoint

    @staticmethod
    def parse_path_params(path_params: dict | None = None) -> dict | None:
        if not path_params:
            return None
        return {
            key: quote(value, safe="")
            for key, value in path_params.items()
            if value is not None
        }

    @property
    def base_url(self) -> str:
        protocol = self.configuration["protocol"]
        host = self.configuration["host"]
        return f"{protocol}://{host.strip('/')}"

    @abstractmethod
    def get_configuration(self) -> BaseConfiguration:
        ...
