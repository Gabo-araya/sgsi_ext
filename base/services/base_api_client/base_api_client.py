import os

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Literal
from urllib.parse import quote

import requests

from base.models import ClientLog

DEFAULT_TIMEOUT = 10
DEFAULT_SCHEME = "https"

Method = Literal["get", "post", "patch", "put", "delete"]


class BaseApiClient(ABC):
    code: str | None = None

    def __init__(self) -> None:
        self.configuration = self.get_configuration()

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
    ) -> requests.Response:
        return self.request(
            "get",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
        )

    def post_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return self.request(
            "post",
            url,
            json=body,
            params=query_params,
        )

    def patch_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self.request(
            "patch",
            endpoint=endpoint,
            path_params=path_params,
            json=body,
            params=query_params,
        )

    def put_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self.request(
            "put",
            endpoint=endpoint,
            path_params=path_params,
            json=body,
            params=query_params,
        )

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
    ) -> requests.Response:
        return self.request(
            "delete",
            endpoint=endpoint,
            path_params=path_params,
        )

    def request(
        self,
        method: Method,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        **kwargs,
    ) -> requests.Response:
        try:
            url = self.get_url(endpoint, path_params)
            log = self.create_log(method, endpoint, url, kwargs.get("json", ""))
            response = self.make_request(method, url, **kwargs)
            self.update_log(log, response)
        except Exception as error:
            log.request_error = str(error)
            log.save()
            raise Exception from error
        else:
            return response

    def update_log(self, log, response):
        log.response_headers = str(response.headers)
        log.response_content = response.text
        log.save()

    def make_request(
        self,
        method: Method,
        url: str,
        **kwargs,
    ):
        return requests.request(
            method, url, timeout=self.configuration["timeout"], **kwargs
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

    def create_log(
        self, method: Method, endpoint: str, url: str, request_body: dict | None
    ):
        return ClientLog.objects.create(
            method=method,
            url=url,
            endpoint=endpoint,
            client_url=self.base_url,
            client_code=self.client_code,
            request_content=request_body,
        )

    def get_configuration(self) -> dict:
        return {
            **self.get_default_configuration(),
            **self.get_extra_configuration(),
        }

    def get_default_configuration(self):
        return {
            "timeout": DEFAULT_TIMEOUT,
            "scheme": DEFAULT_SCHEME,
        }

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
    def client_code(self):
        return self.code or self.__class__.__name__

    @property
    def base_url(self) -> str:
        scheme = self.configuration["scheme"]
        host = self.configuration["host"]
        return f"{scheme}://{host.strip('/')}"

    @abstractmethod
    def get_extra_configuration(self) -> dict:
        ...
