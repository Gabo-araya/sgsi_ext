import logging
import os
import traceback

from typing import Any
from urllib.parse import quote_plus

import requests

from requests.adapters import HTTPAdapter
from requests.adapters import Retry

from api_client.models import ClientConfig

from ....models import ClientLog
from ..errors import DisabledClientError
from ..types import JSONType
from ..types import Method
from ..types import UploadFiles
from .base import BaseApiClient

logger = logging.getLogger("api_clients")


class BlockingApiClient(BaseApiClient):
    """Implementation of blocking methods for the API client."""

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        """
        Makes a GET request to the specified endpoint. This method blocks the thread
        until a response is received.

        Args:
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            query_params: A key-value mapping that is appended to the URL as a query
                          string.
            headers: A key-value mapping of request headers.

        Examples:
            A basic request would be::

                client = ApiClient(...)
                response, error = client.get_blocking(
                    "items/",
                )

            A request using path params, query string and headers would be::

                client = ApiClient(...)
                response, error = client.get_blocking(
                    "items/{id}/",
                    path_params={"id": 1},
                    query_params={"detail": "full", "format": "json"},
                    headers={"Some-Special-Header": "magic"},
                )

            This translates to GET items/1/?detail=full&format=json

        """
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
        """
        Makes a POST request to the specified endpoint. This method blocks the thread
        until a response is received.

        Args:
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            query_params: A key-value mapping that is appended to the URL as a query
                          string.
            headers: A key-value mapping of request headers.
            data: A key-value mapping that is sent to the external service as
                  urlencoded form-data parameters.
            json: Data to be encoded as JSON and sent to the service.
            files: A key-value mapping of filenames and files. It cannot be used along
                   with JSON payloads.

        Examples:
            A basic request would be::

                client = ApiClient(...)
                response, error = client.post_blocking(
                    "items/",
                    data={"name": "ABC", "price": 1000},
                )

            And in turn will generate a POST items/ with the following encoded body::

                name=ABC&price=1000

            A request using path params, query string and JSON data would be::

                client = ApiClient(...)
                response, error = client.get_blocking(
                    "items/{id}/extras",
                    path_params={"id": 1},
                    query_params={"detail": "basic", "format": "json"},
                    json={"name": "ABC", "price": 1000},
                )

            This makes a POST request to items/1/extras?detail=basic&format=json
            Content-Encoding will be set to `application/json` with body::

                {"name": "ABC", "price": 1000}

            A request using path params, and file data would be::

                client = ApiClient(...)
                response, error = client.get_blocking(
                    "items/{id}/picture",
                    path_params={"id": 1},
                    files={"image.jpg": open("file.jpg", "rb")},
                )
        """
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
        """
        Makes a PATCH request to the specified endpoint. This method blocks the thread
        until a response is received.

        Args:
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            query_params: A key-value mapping that is appended to the URL as a query
                          string.
            headers: A key-value mapping of request headers.
            data: A key-value mapping that is sent to the external service as
                  urlencoded form-data parameters.
            json: Data to be encoded as JSON and sent to the service.
            files: A key-value mapping of filenames and files. It cannot be used along
                   with JSON payloads.

        For examples, see the documentation for POST, as the signature is the same.
        """
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
        """
        Makes a PUT request to the specified endpoint. This method blocks the thread
        until a response is received.

        Args:
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            query_params: A key-value mapping that is appended to the URL as a query
                          string.
            headers: A key-value mapping of request headers.
            data: A key-value mapping that is sent to the external service as
                  urlencoded form-data parameters.
            json: Data to be encoded as JSON and sent to the service.
            files: A key-value mapping of filenames and files. It cannot be used along
                   with JSON payloads.

        For examples, see the documentation for POST, as the signature is the same.
        """
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
        """
        Makes a DELETE request to the specified endpoint. This method blocks the thread
        until a response is received.

        Args:
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            headers: A key-value mapping of request headers.
        """
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
        """
        Makes a request to the specified endpoint. You should normally not use this
        method.

        This method accepts all the parameters admitted by requests.Request.

        This method blocks the thread until a response is received.

        Args:
            method: Request method.
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            query_params: A key-value mapping that is appended to the URL as a query
                          string.
            headers: A key-value mapping of request headers.
            data: A key-value mapping that is sent to the external service as
                  urlencoded form-data parameters.
            json: Data to be encoded as JSON and sent to the service.
            files: A key-value mapping of filenames and files. It cannot be used along
                   with JSON payloads.
        """
        if ClientConfig.objects.is_disabled(self.configuration.code):
            return (
                self.empty_response,
                DisabledClientError("Client is disabled and cannot make requests."),
            )

        log: ClientLog = ClientLog.objects.create()
        session = self.get_session()
        try:
            parsed_response = self.perform_request(
                method,
                endpoint,
                path_params,
                session,
                log,
                **kwargs,
            )
        except requests.RequestException as error:
            self.log_exception(log)
            return self.empty_response, error
        else:
            return parsed_response, None
        finally:
            session.close()

    def get_session(self) -> requests.Session:
        session = requests.Session()
        session = self.set_session_retries(session)
        return session

    def set_session_retries(self, session: requests.Session) -> requests.Session:
        total_retries = self.get_total_retries()
        if not total_retries:
            return session
        retries = Retry(total=total_retries)
        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def perform_request(  # noqa: PLR0913
        self,
        method: Method,
        endpoint: str,
        path_params: dict[str, str | int] | None,
        session: requests.Session,
        log: ClientLog,
        **kwargs,
    ):
        request = self.get_request(method, endpoint, path_params, **kwargs)
        prepared_request = request.prepare()
        log.update_from_request(
            request=prepared_request, client_code=self.configuration.code
        )
        response = session.send(prepared_request, timeout=self.configuration.timeout)
        parsed_response = self.parse_response(response)
        log.update_from_response(response=response)
        return parsed_response

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
        log.error = traceback.format_exc()
        log.save()

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

    def get_total_retries(self) -> int:
        return ClientConfig.objects.get_total_retries(self.configuration.code)

    @property
    def base_url(self) -> str:
        scheme = self.configuration.scheme
        host = self.configuration.host
        return f"{scheme}://{host.strip('/')}"
