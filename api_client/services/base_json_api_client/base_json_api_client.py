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
    ) -> tuple[JSONType, int]:
        response = super().get_blocking(endpoint, path_params, query_params)
        return self.get_response_json(response), response.status_code

    def post_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[JSONType, int]:
        response = super().post_blocking(endpoint, path_params, query_params, body)
        return self.get_response_json(response), response.status_code

    def patch_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[JSONType, int]:
        response = super().patch_blocking(endpoint, path_params, query_params, body)
        return self.get_response_json(response), response.status_code

    def put_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[JSONType, int]:
        response = super().put_blocking(endpoint, path_params, query_params, body)
        return self.get_response_json(response), response.status_code

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
    ) -> tuple[JSONType, int]:
        response = super().delete_blocking(endpoint, path_params)
        return self.get_response_json(response), response.status_code

    def get_response_json(self, response: requests.Response) -> JSONType:
        if len(response.content) == 0:
            return None
        return response.json()
