import dataclasses

from django.utils.module_loading import import_string

from api_client.enums import ClientCodes

from .auth import SerializableAuthBase
from .utils import get_fully_qualified_name

DEFAULT_TIMEOUT = 10
DEFAULT_SCHEME = "https"


@dataclasses.dataclass
class ApiClientConfiguration:
    """
    Represents an API client configuration.

    As with SerializableAuthBase, this class needs to be serializable to allow workers
    to initialize the client. Unlike the former, this class does not need overriding.

    Attributes:
        host: Specifies the hostname of the external service and optionally, its API
              prefix.
        code: The internal code of the client that allows for request identification
              in logs. This must be a valid ClientCodes choice.
        scheme: The request scheme to use. http and https are supported.
        timeout: Maximum waiting time in seconds for requests.
        auth: An initialized authentication class, used to authenticate the request.
              It needs to be a serializable object according to the SerializableAuthBase
              definition.

    """

    host: str
    code: ClientCodes
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
