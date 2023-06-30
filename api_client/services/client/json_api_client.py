from typing import Any
from typing import cast

import requests

from .api_client import ApiClient
from .types import JSONType
from .types import Method
from .types import UploadFiles


class JsonApiClient(ApiClient):
    """
    Variant of ApiClient that operates with JSON endpoints.

    It expects JSON from the server and returns parsed responses from it, avoiding the
    need to parse them manually.
    """

    empty_response = None, None

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
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
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
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
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
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
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
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
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
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
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
        kwargs.setdefault("headers", {})
        if kwargs["headers"] is None:
            kwargs["headers"] = {}
        kwargs["headers"].setdefault("Accept", "application/json")

        raw_response, error = super().request_blocking(
            method, endpoint, path_params, **kwargs
        )
        response, status_code = cast(tuple[JSONType, int], raw_response)

        return (response, status_code), error

    def parse_response(self, response: requests.Response):
        if not response.content:
            return None, response.status_code

        return response.json(), response.status_code
