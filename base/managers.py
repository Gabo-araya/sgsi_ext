""" This document defines the Base Manager and BaseQuerySet classes"""


import json

from urllib.parse import urlparse

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Count

import requests


class BaseQuerySet(models.query.QuerySet):
    def to_json(self):
        return json.dumps(list(self.values()), cls=DjangoJSONEncoder)

    def find_duplicates(self, *fields):
        duplicates = self.values(*fields).annotate(Count("id"))
        return duplicates.order_by().filter(id__count__gt=1)


class ClientLogQueryset(models.QuerySet):
    def create_from_request(self, *, client_code: str, request: requests.Request):
        prepared_url = self.prepare_url(request.url, request.params)
        parsed_url = urlparse(prepared_url)
        return self.create(
            method=request.method,
            url=parsed_url.geturl(),
            client_url=f"{parsed_url.scheme}://{parsed_url.hostname}",
            client_code=client_code,
            endpoint=parsed_url.path,
            request_headers=str(request.headers),
            request_content=str(request.data),
        )

    def prepare_url(self, url: str, query_params: dict[str, str]) -> str:
        string_params = [f"{key}={value}" for key, value in query_params.items()]
        if not query_params:
            return url
        return f"{url}?{'&'.join(string_params)}"
