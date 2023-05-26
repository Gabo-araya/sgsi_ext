import dataclasses

from abc import abstractmethod
from dataclasses import dataclass

from django.utils.module_loading import import_string

from requests.auth import AuthBase

from .utils import get_fully_qualified_name

DEFAULT_TIMEOUT = 10
DEFAULT_SCHEME = "https"


class SerializableAuthBase(AuthBase):
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


@dataclass
class ApiClientConfiguration:
    host: str
    code: str
    scheme: str = DEFAULT_SCHEME
    timeout: int = DEFAULT_TIMEOUT
    auth: SerializableAuthBase | None = None

    @classmethod
    def from_serialized_configuration(cls, **kwargs):
        initkwargs = kwargs.copy()

        auth_class = initkwargs.pop("auth_class", None)
        auth_class_config = initkwargs.pop("auth_class_config", {})

        if auth_class is not None:
            auth_klass: type[SerializableAuthBase] = import_string(auth_class)
            initkwargs["auth"] = auth_klass.from_serialized_args(**auth_class_config)

        return cls(**initkwargs)

    def serialize(self):
        """
        Converts an APIClientConfiguration object to a dict that can serialize to JSON.
        """
        client_config = dataclasses.asdict(self)
        if auth := client_config.pop("auth", None):
            client_config["auth_class"] = get_fully_qualified_name(auth.__class__)
            client_config["auth_class_config"] = auth.get_init_kwargs()

        return client_config
