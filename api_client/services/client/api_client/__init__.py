from .blocking import BlockingApiClient
from .non_blocking import NonBlockingApiClient


class ApiClient(BlockingApiClient, NonBlockingApiClient):
    pass


__all__ = ["ApiClient", "BlockingApiClient", "NonBlockingApiClient"]
