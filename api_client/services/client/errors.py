from requests import RequestException


class InvalidCallbackError(Exception):
    """Raised when a callback function is unusable for non-blocking requests."""


class ClientConfigurationError(Exception):
    """Raised when trying to create a client instance with invalid configuration."""


class DisabledClientError(RequestException):
    """Raised when attempting to request to a disabled client."""
