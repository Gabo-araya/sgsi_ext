import os
import traceback

from typing import Any
from urllib.parse import quote_plus

import requests

from api_client.models import ClientLog

from .config import ApiClientConfiguration
from .handlers import default_success_handler
from .tasks import run_nonblocking_request
from .types import Callback
from .types import JSONType
from .types import Method
from .types import UploadFiles
from .utils import get_fully_qualified_name
from .utils import make_configuration_dict
from .utils import validate_nonblocking_callbacks


class BaseApiClient:
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


class BlockingApiClient(BaseApiClient):
    def __init__(self, configuration: ApiClientConfiguration) -> None:
        self.configuration = configuration

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
    ) -> tuple[requests.Response, requests.RequestException | None]:
        return self.request_blocking(
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
        return self.request_blocking(
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
        return self.request_blocking(
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
        return self.request_blocking(
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
        return self.request_blocking(
            "delete",
            endpoint=endpoint,
            path_params=path_params,
        )

    def request_blocking(
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

        if hasattr(self.configuration, "auth"):
            request.auth = self.configuration.auth

        return request


class NonBlockingApiClient(BaseApiClient):
    def __init__(self, configuration: ApiClientConfiguration) -> None:
        self.configuration = configuration

    def get(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
    ):
        self.request(
            "get",
            endpoint,
            path_params=path_params,
            query_params=query_params,
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
            on_success=on_success,
            on_error=on_error,
        )

    def delete(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        *,
        on_success: Callback = default_success_handler,
        on_error: Callback,
    ):
        self.request(
            "delete",
            endpoint,
            path_params=path_params,
            on_success=on_success,
            on_error=on_error,
            query_params=query_params,
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

        client_config = make_configuration_dict(self.configuration)

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


class ApiClient(BlockingApiClient, NonBlockingApiClient):
    pass
