from typing import Any

import requests

from base.services.base_api_client import BaseApiClient


class BaseJsonApiClient(BaseApiClient):
    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], int]:
        response = super().get_blocking(endpoint, path_params, query_params)
        return self.get_response_json(response), response.status_code

    def post_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], int]:
        response = super().post_blocking(endpoint, path_params, query_params, body)
        return self.get_response_json(response), response.status_code

    def patch_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], int]:
        response = super().patch_blocking(endpoint, path_params, query_params, body)
        return self.get_response_json(response), response.status_code

    def put_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], int]:
        response = super().put_blocking(endpoint, path_params, query_params, body)
        return self.get_response_json(response), response.status_code

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], int]:
        response = super().delete_blocking(endpoint, path_params)
        return self.get_response_json(response), response.status_code

    def get_response_json(self, response: requests.Response) -> dict[str, Any]:
        if len(response.content) == 0:
            return {}
        return response.json()
