from dataclasses import dataclass

from requests.auth import AuthBase

DEFAULT_TIMEOUT = 10
DEFAULT_SCHEME = "https"


@dataclass
class ApiClientConfiguration:
    host: str
    code: str
    scheme: str = DEFAULT_SCHEME
    timeout: int = DEFAULT_TIMEOUT
    auth: AuthBase | None = None
