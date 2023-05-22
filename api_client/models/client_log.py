from urllib.parse import urlparse

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import requests

from api_client.managers import ClientLogQueryset
from base.serializers import StringFallbackJSONEncoder

ClientLogManager = models.Manager.from_queryset(ClientLogQueryset)


class ClientLog(models.Model):
    class MethodOptions(models.TextChoices):
        GET = "GET", _("GET")
        POST = "POST", _("POST")
        PUT = "PUT", _("PUT")
        PATCH = "PATCH", _("PATCH")
        DELETE = "DELETE", _("DELETE")

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("creation date"),
        verbose_name=_("created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        help_text=_("edition date"),
        verbose_name=_("updated at"),
    )
    error = models.TextField(
        verbose_name=_("error"),
    )
    method = models.CharField(
        max_length=10,
        verbose_name=_("method"),
        choices=MethodOptions.choices,
    )
    url = models.TextField(
        verbose_name=_("url"),
    )
    endpoint = models.TextField(
        verbose_name=_("endpoint"),
    )
    client_url = models.TextField(
        verbose_name=_("client url"),
    )
    client_code = models.TextField(
        verbose_name=_("client code"),
    )
    request_time = models.DateTimeField(
        help_text=_("request time"),
        verbose_name=_("request time"),
        null=True,
    )
    request_headers = models.JSONField(
        verbose_name=_("headers"),
        encoder=StringFallbackJSONEncoder,
        default=dict,
    )
    request_content = models.TextField(
        verbose_name=_("content"),
    )
    response_time = models.DateTimeField(
        help_text=_("response time"),
        verbose_name=_("response time"),
        null=True,
    )
    response_headers = models.JSONField(
        verbose_name=_("headers"),
        encoder=StringFallbackJSONEncoder,
        default=dict,
    )
    response_content = models.TextField(
        verbose_name=_("content"),
    )
    response_status_code = models.IntegerField(
        verbose_name=_("status code"),
        null=True,
    )

    objects = ClientLogManager()

    def __str__(self) -> str:
        return f"{self.client_code}: {self.method.upper()} {self.url}"

    def update_from_response(self, *, response: requests.Response):
        self.response_time = timezone.now()
        self.response_headers = response.headers
        self.response_content = response.text
        self.response_status_code = response.status_code
        self.save()

    def update_from_request(
        self, *, request: requests.PreparedRequest, client_code: str
    ):
        parsed_url = urlparse(request.url)
        self.method = request.method.upper()
        self.url = parsed_url.geturl()
        self.client_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        self.client_code = client_code
        self.endpoint = parsed_url.path
        self.request_time = timezone.now()
        self.request_headers = request.headers
        self.request_content = str(request.body)
        self.save()
