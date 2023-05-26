from api_client.enums import ClientCodes

from ..config import ApiClientConfiguration


class BaseApiClient:
    def __init__(self, configuration: ApiClientConfiguration) -> None:
        self.configuration = configuration
        self.validate_configuration()

    def validate_configuration(self) -> None:
        if not isinstance(self.configuration.code, ClientCodes):
            msg = f"Invalid client code: {self.configuration.code}"
            raise TypeError(msg)
