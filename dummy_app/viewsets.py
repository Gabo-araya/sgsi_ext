from typing import TypedDict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class DummyDataType(TypedDict):
    pk: int
    name: str


class DummyViewset(ViewSet):
    DUMMY_DATA: list[DummyDataType] = [
        {"pk": 1, "name": "Dummy 1"},
        {"pk": 2, "name": "Dummy 2"},
    ]

    def retrieve(self, request, pk=None):
        dummy = self.find_dummy(pk)
        if dummy:
            return Response(dummy)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def find_dummy(self, pk: int) -> dict:
        for dummy in self.DUMMY_DATA:
            if dummy["pk"] == pk:
                return dummy
        return None
