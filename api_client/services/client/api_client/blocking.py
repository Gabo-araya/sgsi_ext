import logging
import os
import traceback

from typing import Any
from urllib.parse import quote_plus

import requests

from api_client.models import ClientConfig

from ....models import ClientLog
from ..errors import DisabledClientError
from ..types import JSONType
from ..types import Method
from ..types import UploadFiles
from .base import BaseApiClient

logger = logging.getLogger("api_clients")


class BlockingApiClient(BaseApiClient):
    empty_response = requests.Response()

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request_blocking(
            "get",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
            headers=headers,
        )

    def post_blocking(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request_blocking(
            "post",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
            data=data,
            json=json,
            files=files,
            headers=headers,
        )

    def patch_blocking(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request_blocking(
            "patch",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
            data=data,
            json=json,
            files=files,
            headers=headers,
        )

    def put_blocking(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request_blocking(
            "put",
            endpoint=endpoint,
            path_params=path_params,
            params=query_params,
            data=data,
            json=json,
            files=files,
            headers=headers,
        )

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request_blocking(
            "delete",
            endpoint=endpoint,
            path_params=path_params,
            headers=headers,
        )

    def request_blocking(
        self,
        method: Method,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        **kwargs,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        if ClientConfig.objects.is_disabled(self.configuration.code):
            return (
                self.empty_response,
                DisabledClientError("Client is disabled and cannot make requests."),
            )

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
            parsed_response = self.parse_response(response)
            log.update_from_response(response=response)
        except requests.RequestException as error:
            self.log_exception(log)
            log.error = traceback.format_exc()
            log.save()
            return self.empty_response, error
        else:
            return parsed_response, None
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

        if hasattr(self.configuration, "auth"):
            request.auth = self.configuration.auth

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

    def log_exception(self, log: ClientLog):
        logger.exception(
            "Client Integration Error",
            extra={
                **log.to_dict(),
                "timeout": self.configuration.timeout,
            },
        )

    def parse_response(self, response: requests.Response):
        """
        Converts the raw response into the expected output format.
        By default, it returns the response as-is.
        """
        return response

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
