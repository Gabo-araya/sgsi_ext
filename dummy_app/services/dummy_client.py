from rest_framework import status

from base.services import BaseJsonApiClient
from base.services.base_api_client.base_api_client import BaseConfiguration


class DummyError(Exception):
    ...


class DummyClient(BaseJsonApiClient):
    def get_configuration(self) -> BaseConfiguration:
        return {
            "host": "localhost:8000/api/v1",
            "protocol": "http",
            "timeout": 10,
        }

    def get_dummies(self):
        data, status_code = self.get_blocking("/dummy/")
        if status_code != status.HTTP_200_OK:
            msg = "Error getting dummies"
            raise DummyError(msg)
        return data

    def get_dummy(self, pk):
        data, status_code = self.get_blocking(
            "/dummy/{pk}/",
            path_params={"pk": pk},
            query_params={"TEST": "dsal😱kjdsäßðó®öé"},
        )
        if status_code != status.HTTP_200_OK:
            msg = f"Error getting dummy {pk}"
            raise DummyError(msg)
        return data

    def create_dummy(self, name):
        data, status_code = self.post_blocking("/dummy/", body={"name": name})
        if status_code != status.HTTP_201_CREATED:
            msg = f"Error creating dummy {name}"
            raise DummyError(msg)
        return data

    def update_dummy(self, pk, name):
        data, status_code = self.put_blocking(
            "/dummy/{pk}/", path_params={"pk": "153"}, body={"name": name}
        )
        if status_code != status.HTTP_200_OK:
            msg = f"Error updating dummy {pk}"
            raise DummyError(msg)
        return data

    def delete_dummy(self, pk):
        data, status_code = self.delete_blocking(
            "/dummy/{pk}/", path_params={"pk": "153"}
        )
        if status_code != status.HTTP_204_NO_CONTENT:
            msg = f"Error deleting dummy {pk}"
            raise DummyError(msg)
        return data
