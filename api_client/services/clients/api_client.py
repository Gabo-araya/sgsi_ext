import os
import traceback

from dataclasses import dataclass
from typing import Any
from urllib.parse import quote_plus

import requests

from requests.auth import AuthBase

from api_client.models import ClientLog

from .types import JSONType
from .types import Method
from .types import UploadFiles

DEFAULT_TIMEOUT = 10
DEFAULT_SCHEME = "https"


@dataclass
class ApiClientConfiguration:
    host: str
    code: str
    scheme: str = DEFAULT_SCHEME
    timeout: int = DEFAULT_TIMEOUT
    auth: AuthBase | None = None


class ApiClient:
    def __init__(self, configuration: ApiClientConfiguration) -> None:
        self.configuration = configuration

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request(
            "get",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
        )

    def post_blocking(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request(
            "post",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
            data=data,
            json=json,
            files=files,
        )

    def patch_blocking(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request(
            "patch",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
            data=data,
            json=json,
            files=files,
        )

    def put_blocking(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request(
            "put",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
            data=data,
            json=json,
            files=files,
        )

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
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
    ) -> tuple[requests.Response, requests.RequestException | None]:
        log: ClientLog = ClientLog.objects.create()
        session = requests.Session()
        try:
            request = self.get_request(method, endpoint, path_params, **kwargs)
            prepared_request = request.prepare()
            log.update_from_request(
                request=prepared_request, client_code=self.configuration.code
            )
            response = session.send(
                prepared_request, timeout=self.configuration.timeout
            )
            log.update_from_response(response=response)
        except requests.RequestException as error:
            log.error = traceback.format_exc()
            log.save()
            return requests.Response(), error
        else:
            return response, None
        finally:
            session.close()

    def get_request(
        self,
        method: Method,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        **kwargs,
    ) -> requests.Request:
        url = self.get_url(endpoint, path_params)
        request = requests.Request(method, url, **kwargs)

        if auth := self.configuration.auth:
            request.auth = auth

        return request

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
            key: quote_plus(str(value))
            for key, value in path_params.items()
            if value is not None
        }

    @property
    def base_url(self) -> str:
        scheme = self.configuration.scheme
        host = self.configuration.host
        return f"{scheme}://{host.strip('/')}"
