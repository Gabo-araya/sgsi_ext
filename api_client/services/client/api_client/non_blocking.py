from typing import Any

from ..config import ApiClientConfiguration
from ..handlers import default_success_handler
from ..tasks import run_nonblocking_request
from ..types import Callback
from ..types import JSONType
from ..types import Method
from ..utils import get_fully_qualified_name
from ..utils import validate_nonblocking_callbacks


class NonBlockingApiClient:
    def __init__(self, configuration: ApiClientConfiguration) -> None:
        self.configuration = configuration

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
        query_params: dict[str, str | int] | None = None,
        headers: dict[str, Any] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
    ):
        self.request(
            "delete",
            endpoint,
            path_params=path_params,
            query_params=query_params,
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
