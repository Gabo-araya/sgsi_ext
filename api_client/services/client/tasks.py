from typing import TYPE_CHECKING
from typing import Any

from django.utils.module_loading import import_string

from project.celeryconf import app

from .config import ApiClientConfiguration
from .types import Callback
from .types import JSONType
from .types import Method

if TYPE_CHECKING:
    from api_client.services import BaseApiClient


@app.task
def run_nonblocking_request(  # noqa: PLR0913
    client_class: str,
    client_configuration: dict,
    method: Method,
    endpoint: str,
    on_success: str,
    on_error: str,
    path_params: dict[str, str | int] | None = None,
    query_params: dict[str, str | int] | None = None,
    data: dict[str, Any] | None = None,
    json: JSONType = None,
    headers=None,
):
    """
    This task is run in a worker and handles all non-blocking requests outside the
    request-response cycle. It takes a request, a client class name and configuration,
    initializes the respective client, sends the request and dispatches the defined
    error or success handlers.

    You should normally not use this function as it is called automatically by
    APIClient in non-blocking mode.

    Args:
        client_class: The fully qualified name of the APIClient class, including its
                      module name.
        client_configuration: A dictionary containing the necessary parameters to
                              initialize the API client.
        method: Request method.
        endpoint: Endpoint to request. This string can contain parameters enclosed by
                  brackets. Those parameters will be substituted later.
        on_success: Fully qualified name of the success handler. It must be the name
                    of a function receiving a 2-tuple of response and error.
        on_error: Fully qualified name of the error handler. It must be the name
                    of a function receiving a 2-tuple of response and error.

    Keyword Args:
        path_params: A mapping of parameter names and values. Keys must match with
                     parameters defined in the endpoint.
        query_params: A key-value mapping that is appended to the URL as a query string.
        data: A key-value mapping that is sent to the external service as
              urlencoded form-data parameters.
        json: Data to be encoded as JSON and sent to the service.
        headers: A key-value mapping of request headers.
    """
    client_klass: type[BaseApiClient] = import_string(client_class)
    success_handler: Callback = import_string(on_success)
    error_handler: Callback = import_string(on_error)

    client_config = ApiClientConfiguration.from_serialized_configuration(
        **client_configuration
    )
    client = client_klass(client_config)

    response, error = client.request_blocking(
        method,
        endpoint,
        path_params,
        params=query_params,
        data=data,
        json=json,
        headers=headers,
    )

    if error:
        error_handler(response, error)
    else:
        success_handler(response, error)
