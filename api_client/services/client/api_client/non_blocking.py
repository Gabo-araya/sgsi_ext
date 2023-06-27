from typing import Any

from ..handlers import default_success_handler
from ..tasks import run_nonblocking_request
from ..types import Callback
from ..types import JSONType
from ..types import Method
from ..utils import get_fully_qualified_name
from ..utils import validate_nonblocking_callbacks
from .base import BaseApiClient


class NonBlockingApiClient(BaseApiClient):
    """Implementation of non-blocking methods for the API client."""

    def __new__(cls, *args, **kwargs):
        if cls is NonBlockingApiClient:
            msg = "This class is not meant to be used directly. Use ApiClient instead."
            raise TypeError(msg)
        return super().__new__(cls)

    def get(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        headers: dict[str, Any] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
    ):
        """
        Makes a GET request to the specified endpoint. This method and its response will
        be handled on a separate worker.

        Args:
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            query_params: A key-value mapping that is appended to the URL as a query
                          string.
            headers: A key-value mapping of request headers.
            on_success: Fully qualified name of the success handler. It must be the name
                        of a function receiving a 2-tuple of response and error.
            on_error: Fully qualified name of the error handler. It must be the name
                        of a function receiving a 2-tuple of response and error.

        Examples:
            Assuming `success_handler` and `error_handler` are valid functions, a basic
            request would be::

                client = ApiClient(...)
                client.get(
                    "products/",
                    on_success=success_handler
                )

            A request using path params, query string and headers would be::

                client = ApiClient(...)
                client.get(
                    "items/{id}/",
                    path_params={"id": 1},
                    query_params={"detail": "full", "format": "json"},
                    headers={"Some-Special-Header": "magic"},
                    on_success=success_handler,
                    on_error=error_handler,
                )
        """
        self.request(
            "get",
            endpoint,
            path_params=path_params,
            query_params=query_params,
            headers=headers,
            on_success=on_success,
            on_error=on_error,
        )

    def post(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        headers: dict[str, Any] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
    ):
        """
        Makes a POST request to the specified endpoint. This method and its response
        will be handled on a separate worker.

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
            on_success: Fully qualified name of the success handler. It must be the name
                        of a function receiving a 2-tuple of response and error.
            on_error: Fully qualified name of the error handler. It must be the name
                        of a function receiving a 2-tuple of response and error.

        Examples:
            Assuming `success_handler` and `error_handler` are valid functions, a basic
            request would be::

                client = ApiClient(...)
                response, error = client.post_blocking(
                    "items/",
                    data={"name": "ABC", "price": 1000},
                    on_success=success_handler
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
                    on_success=success_handler,
                    on_error=error_handler,
                )

            This makes a POST request to items/1/extras?detail=basic&format=json
            Content-Encoding will be set to `application/json` with body::

                {"name": "ABC", "price": 1000}

        """
        self.request(
            "post",
            endpoint,
            path_params=path_params,
            query_params=query_params,
            data=data,
            json=json,
            headers=headers,
            on_success=on_success,
            on_error=on_error,
        )

    def patch(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        headers: dict[str, Any] | None = None,
        *,
        on_success: Callback,
        on_error: Callback,
    ):
        """
        Makes a PATCH request to the specified endpoint. This method and its response
        will be handled on a separate worker.

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
            on_success: Fully qualified name of the success handler. It must be the name
                        of a function receiving a 2-tuple of response and error.
            on_error: Fully qualified name of the error handler. It must be the name
                        of a function receiving a 2-tuple of response and error.

        For examples, see the documentation for POST, as the signature is the same.
        """
        self.request(
            "patch",
            endpoint,
            path_params=path_params,
            query_params=query_params,
            data=data,
            json=json,
            headers=headers,
            on_success=on_success,
            on_error=on_error,
        )

    def put(  # noqa: PLR0913
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        headers: dict[str, Any] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
    ):
        """
        Makes a PUT request to the specified endpoint. This method and its response
        will be handled on a separate worker.

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
            on_success: Fully qualified name of the success handler. It must be the name
                        of a function receiving a 2-tuple of response and error.
            on_error: Fully qualified name of the error handler. It must be the name
                        of a function receiving a 2-tuple of response and error.

        For examples, see the documentation for POST, as the signature is the same.
        """
        self.request(
            "put",
            endpoint,
            path_params=path_params,
            query_params=query_params,
            data=data,
            json=json,
            headers=headers,
            on_success=on_success,
            on_error=on_error,
        )

    def delete(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        headers: dict[str, Any] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
    ):
        """
        Makes a DELETE request to the specified endpoint. This method and its response
        will be handled on a separate worker.

        Args:
            endpoint: Endpoint to request. This string can contain parameters enclosed
                      by brackets. Those parameters will be substituted later.

        Keyword Args:
            path_params: A mapping of parameter names and values. Keys must match with
                         parameters defined in the endpoint.
            headers: A key-value mapping of request headers.
            on_success: Fully qualified name of the success handler. It must be the name
                        of a function receiving a 2-tuple of response and error.
            on_error: Fully qualified name of the error handler. It must be the name
                        of a function receiving a 2-tuple of response and error.

        For examples, see the documentation for POST, as the signature is the same.
        """
        self.request(
            "delete",
            endpoint,
            path_params=path_params,
            headers=headers,
            on_success=on_success,
            on_error=on_error,
        )

    def request(
        self,
        method: Method,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
        **kwargs,
    ):
        """
        Makes a request to the specified endpoint. You should normally not use this
        method.

        This method accepts all the parameters admitted by requests.Request except for
        `files`, which is not supported for non-blocking requests.

        This method will not block the thread and responses are handled in a separate
        worker.

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
        """
        validate_nonblocking_callbacks(on_success, on_error)

        # Generate fully qualified names for handlers and class
        client_name = get_fully_qualified_name(self.__class__)
        success_handler_name = get_fully_qualified_name(on_success)
        error_handler_name = get_fully_qualified_name(on_error)

        client_config = self.configuration.serialize()

        run_nonblocking_request.delay(
            client_name,
            client_config,
            method,
            endpoint,
            success_handler_name,
            error_handler_name,
            path_params,
            **kwargs,
        )
