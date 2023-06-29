from abc import ABCMeta
from abc import abstractmethod

from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth


class SerializableAuthBase(AuthBase, metaclass=ABCMeta):
    """
    Variation of requests.auth.AuthBase that allows serialization of
    initialization parameters.

    Non-blocking requests are run outside the request-response cycle and may be run
    on a different worker and therefore there exists a need to pass authentication data
    to workers in order to make valid requests.

    Implementations of this class must define `get_init_kwargs` to allow non-blocking
    methods to correctly create instances of this class in workers.
    """

    @abstractmethod
    def get_init_kwargs(self):
        """
        Returns a dictionary with its initialization parameters.

        This method is invoked by NonBlockingApiClient to retrieve the init kwargs
        necessary to initialize the client on the worker, so they need to be
        serializable.
        """
        raise NotImplementedError

    @classmethod
    def from_serialized_args(cls, **kwargs):
        """
        Initializes the class from a dictionary of values.

        Used by run_nonblocking_request to initialize the class on the worker. If your
        authentication class does not use non-serializable arguments, you can use the
        default implementation. Otherwise, you must override this class to ensure
        objects can be properly created before initializing the auth class.
        """
        # noinspection PyArgumentList
        return cls(**kwargs)


class BasicAuth(SerializableAuthBase, HTTPBasicAuth):
    """Basic user-password authentication."""

    def get_init_kwargs(self):
        return {"username": self.username, "password": self.password}


class BearerAuth(SerializableAuthBase):
    """Basic bearer authentication."""

    def __init__(self, token, auth_type="Bearer"):
        self.token = token
        self.auth_type = auth_type

    def __eq__(self, other):
        return all(
            [
                self.token == getattr(other, "token", None),
                self.auth_type == getattr(other, "auth_type", None),
            ]
        )

    def __ne__(self, other):
        return not self == other

    def __call__(self, request):
        request.headers["Authorization"] = f"{self.auth_type} {self.token}"
        return request

    def get_init_kwargs(self):
        return {"token": self.token, "auth_type": self.auth_type}
