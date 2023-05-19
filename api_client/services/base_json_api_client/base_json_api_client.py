from typing import Any

import requests

from api_client.services import BaseApiClient

JSONType = str | int | float | bool | None | dict[str, "JSONType"] | list["JSONType"]


class BaseJsonApiClient(BaseApiClient):
    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
    ) -> tuple[tuple[JSONType, int], None] | tuple[
        tuple[None, None], requests.RequestException
    ]:
        response, error = super().get_blocking(endpoint, path_params, query_params)
        return self.process_response(response, error)

    def post_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[tuple[JSONType, int], None] | tuple[
        tuple[None, None], requests.RequestException
    ]:
        response, error = super().post_blocking(
            endpoint, path_params, query_params, body
        )
        return self.process_response(response, error)

    def patch_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[tuple[JSONType, int], None] | tuple[
        tuple[None, None], requests.RequestException
    ]:
        response, error = super().patch_blocking(
            endpoint, path_params, query_params, body
        )
        return self.process_response(response, error)

    def put_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[tuple[JSONType, int], None] | tuple[
        tuple[None, None], requests.RequestException
    ]:
        response, error = super().put_blocking(
            endpoint, path_params, query_params, body
        )
        return self.process_response(response, error)

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
    ) -> tuple[tuple[JSONType, int], None] | tuple[
        tuple[None, None], requests.RequestException
    ]:
        response, error = super().delete_blocking(endpoint, path_params)
        return self.process_response(response, error)

    def process_response(
        self,
        response: requests.Response | None,
        error: requests.RequestException | None,
    ) -> tuple[tuple[JSONType, int], None] | tuple[
        tuple[None, None], requests.RequestException
    ]:
        if response:
            return (self.get_response_json(response), response.status_code), error
        return (None, None), error

    def get_response_json(self, response: requests.Response) -> JSONType:
        if len(response.content) == 0:
            return None
        return response.json()
