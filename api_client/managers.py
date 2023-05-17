from urllib.parse import quote_plus
from urllib.parse import urlencode
from urllib.parse import urlparse

from django.db import models
from django.utils import timezone

import requests


def prepare_url(url: str, query_params: dict[str, str]) -> str:
    if not query_params:
        return url
    string_params = urlencode(query_params, quote_via=quote_plus)
    return f"{url}?{string_params}"


class ClientLogQueryset(models.QuerySet):
    def create_from_request(self, *, client_code: str, request: requests.Request):
        prepared_url = prepare_url(request.url, request.params)
        parsed_url = urlparse(prepared_url)
        return self.create(
            method=request.method,
            url=parsed_url.geturl(),
            client_url=f"{parsed_url.scheme}://{parsed_url.hostname}",
            client_code=client_code,
            endpoint=parsed_url.path,
            request_time=timezone.now(),
            request_headers=str(request.headers),
            request_content=str(request.data),
        )

    def old(self):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        return self.filter(created_at__lt=one_year_ago)
