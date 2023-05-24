from http import HTTPStatus

from requests.auth import AuthBase

from api_client.services.clients import ApiClientConfiguration
from api_client.services.clients import JsonApiClient


class DummyError(Exception):
    ...


class SimpleTokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, "token", None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["Authorization"] = f"DummyToken {self.token}"
        return r


class DummyIntegrationService:
    def __init__(self) -> None:
        configuration = ApiClientConfiguration(
            code="dummy_integration_service",
            scheme="http",
            host="localhost:8000/api/v1",
            auth=SimpleTokenAuth,
        )
        self.api_client = JsonApiClient(configuration)

    def get_dummies(self):
        (data, status_code), error = self.api_client.get_blocking("/dummy/")
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = "Error getting dummies"
            raise DummyError(msg)
        return data

    def get_dummy(self, pk):
        (data, status_code), error = self.api_client.get_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = f"Error getting dummy {pk}"
            raise DummyError(msg)
        return data

    def create_dummy(self, name):
        (data, status_code), error = self.api_client.post_blocking(
            "/dummy/", json={"name": name}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.CREATED:
            msg = f"Error creating dummy {name}"
            raise DummyError(msg)
        return data

    def update_dummy(self, pk, name):
        (data, status_code), error = self.api_client.put_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}, json={"name": name}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = f"Error updating dummy {pk}"
            raise DummyError(msg)
        return data

    def delete_dummy(self, pk):
        (data, status_code), error = self.api_client.delete_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.NO_CONTENT:
            msg = f"Error deleting dummy {pk}"
            raise DummyError(msg)
        return data
