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
            data=body,
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
            data=body,
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
            data=body,
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
            request = self.get_request(method, url, **kwargs)
            log = self.create_log(request)
            session = requests.Session()
            response = session.send(
                request.prepare(), timeout=self.configuration["timeout"]
            )
            log.update_from_response(response)
        except Exception as error:
            if isinstance(log, ClientLog):
                log.response_error = str(error)
                log.save()
            raise Exception from error
        else:
            return response

    def create_log(self, request: requests.Request) -> ClientLog:
        return ClientLog.objects.create_from_request(
            request=request, client_code=self.client_code
        )

    def get_request(self, method: Method, url: str, **kwargs) -> requests.Request:
        return requests.Request(
            method,
            url,
            **kwargs,
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
