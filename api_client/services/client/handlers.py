"""Default error handlers"""

import requests


def default_success_handler(
    response: requests.Response, error: requests.RequestException | None
):
    """Default success handler for non-blocking requests. It does nothing by default."""
