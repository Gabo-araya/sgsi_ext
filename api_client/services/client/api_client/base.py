from api_client.enums import ClientCodes

from ..config import ApiClientConfiguration


class BaseApiClient:
    def __init__(self, configuration: ApiClientConfiguration) -> None:
        self.configuration = configuration
        self.validate_configuration()

    def validate_configuration(self) -> None:
        # Try coercing value into an enum one. If this fail then raise an error.
        # This is done to support the non-blocking implementation which serializes
        # the enum into a string.
        try:
            ClientCodes(self.configuration.code)
        except ValueError as e:
            msg = f"Invalid client code: {self.configuration.code}"
            raise TypeError(msg) from e
