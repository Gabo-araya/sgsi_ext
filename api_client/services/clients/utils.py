import dataclasses
import inspect

from .config import ApiClientConfiguration


def get_fully_qualified_name(obj):
    return f"{obj.__module__}.{obj.__qualname__}"


def make_configuration_dict(configuration: ApiClientConfiguration):
    """
    Converts an APIClientConfiguration object to a dict that can serialize to JSON.
    """
    client_config = dataclasses.asdict(configuration)
    if "auth" in client_config:
        # TODO: implement a way to serialize AuthBase object initialization parameters
        del client_config["auth"]
    return client_config


def validate_callback(callback):
    if not callable(callback):
        msg = "Handler is not callable."
        raise TypeError(msg)
    if inspect.ismethod(callback):
        msg = "Bound methods cannot be used as handlers."
        raise ValueError(msg)
    if callback.__name__ == "<lambda>":
        msg = "Lambdas are not serializable and cannot be used as handlers."
        raise TypeError(msg)


def validate_nonblocking_callbacks(on_success, on_error):
    """
    Ensures result handlers for methods meet the following conditions:
        - They are callable
        - They're not lambdas
        - They're not bound methods
    """
    try:
        validate_callback(on_success)
    except (TypeError, ValueError) as e:
        raise type(e)("Invalid success handler: " + str(e)) from e
    try:
        validate_callback(on_error)
    except (TypeError, ValueError) as e:
        raise type(e)("Invalid error handler: " + str(e)) from e
