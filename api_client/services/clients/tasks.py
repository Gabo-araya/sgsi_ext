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
):
    client_klass: type[BaseApiClient] = import_string(client_class)
    success_handler: Callback = import_string(on_success)
    error_handler: Callback = import_string(on_error)

    client_config = ApiClientConfiguration(**client_configuration)
    client = client_klass(client_config)

    response, error = client.request_blocking(
        method, endpoint, path_params, params=query_params, data=data, json=json
    )

    if error:
        error_handler(response, error)
    else:
        success_handler(response, error)
