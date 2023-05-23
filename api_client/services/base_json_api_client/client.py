from typing import Any

import requests

from api_client.services import BaseApiClient
from api_client.services.base_api_client.types import JSONType
from api_client.services.base_api_client.types import UploadFiles


class BaseJsonApiClient(BaseApiClient):
    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
        response, error = super().get_blocking(endpoint, path_params, query_params)
        return (self.get_response_json(response), response.status_code), error

    def post_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
        response, error = super().post_blocking(
            endpoint, path_params, query_params, data, json, files
        )
        return (self.get_response_json(response), response.status_code), error

    def patch_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
        response, error = super().patch_blocking(
            endpoint, path_params, query_params, data, json, files
        )
        return (self.get_response_json(response), response.status_code), error

    def put_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
        query_params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
        json: JSONType = None,
        files: UploadFiles | None = None,
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
        response, error = super().put_blocking(
            endpoint, path_params, query_params, data, json, files
        )
        return (self.get_response_json(response), response.status_code), error

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, str | int] | None = None,
    ) -> tuple[tuple[JSONType, int], requests.RequestException | None]:
        response, error = super().delete_blocking(endpoint, path_params)
        return (self.get_response_json(response), response.status_code), error

    @staticmethod
    def get_response_json(response: requests.Response) -> JSONType:
        if not response.content:
            return None
        return response.json()
