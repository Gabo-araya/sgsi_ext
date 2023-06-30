from typing import TypedDict
from uuid import uuid4

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.models import User


class DummyTokenAuthentication(TokenAuthentication):
    keyword = "DummyToken"
    secret = "thisismagnetbestkeptsecretpleasedonotcopy(c)magnet"  # noqa: S105

    def get_secret(self):
        return self.secret

    def get_model(self):
        return User.objects.first()

    def authenticate_credentials(self, key):
        if key != self.secret:
            msg = "Invalid token."
            raise AuthenticationFailed(msg)

        return self.get_model(), key


class DummyData(TypedDict):
    pk: int
    name: str


class DummyViewset(ViewSet):
    DUMMY_DATA: list[DummyData] = [
        {"pk": "1", "name": "Dummy 1"},
        {"pk": "2", "name": "Dummy 2"},
    ]

    def create(self, request, *args, **kwargs):
        dummy = {"pk": str(uuid4()), "name": request.data["name"]}
        self.DUMMY_DATA.append(dummy)
        return Response(dummy, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):  # noqa: A003
        return Response(self.DUMMY_DATA)

    def retrieve(self, request, pk=None, **kwargs):
        dummy = self.find_dummy(pk)
        if dummy:
            return Response(dummy)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, **kwargs):
        dummy = self.find_dummy(pk)
        if dummy:
            dummy["name"] = request.data["name"]
            return Response(dummy)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, **kwargs):
        dummy = self.find_dummy(pk)
        if dummy:
            self.DUMMY_DATA.remove(dummy)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def find_dummy(self, pk: str) -> dict:
        for dummy in self.DUMMY_DATA:
            if dummy["pk"] == pk:
                return dummy
        return None


class DummyAuthenticatedViewset(DummyViewset):
    authentication_classes = [DummyTokenAuthentication]
    permission_classes = [IsAuthenticated]
