import inspect


class InvalidCallbackError(Exception):
    pass


def get_fully_qualified_name(obj):
    return f"{obj.__module__}.{obj.__qualname__}"


def validate_callback(callback):
    if not callable(callback):
        msg = "Handler is not callable."
        raise InvalidCallbackError(msg)
    if inspect.ismethod(callback):
        msg = "Bound methods cannot be used as handlers."
        raise InvalidCallbackError(msg)
    if callback.__name__ == "<lambda>":
        msg = "Lambdas are not serializable and cannot be used as handlers."
        raise InvalidCallbackError(msg)


def validate_nonblocking_callbacks(on_success, on_error):
    """
    Ensures result handlers for methods meet the following conditions:
        - They are callable
        - They're not lambdas
        - They're not bound methods
    """
    try:
        validate_callback(on_success)
    except InvalidCallbackError as e:
        raise InvalidCallbackError("Invalid success handler: " + str(e)) from e
    try:
        validate_callback(on_error)
    except InvalidCallbackError as e:
        raise InvalidCallbackError("Invalid error handler: " + str(e)) from e
