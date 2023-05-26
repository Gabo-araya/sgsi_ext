from __future__ import annotations

from urllib.parse import urlparse

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import requests

from api_client.enums import ClientCodes
from api_client.managers import ClientLogQueryset
from base.serializers import StringFallbackJSONEncoder
from messaging import email_manager

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
        choices=ClientCodes.choices,
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
    error = models.TextField(
        verbose_name=_("error"),
    )
    error_email_sent = models.BooleanField(
        verbose_name=_("error email sent"),
        default=False,
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
        self, *, request: requests.PreparedRequest, client_code: ClientCodes
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

    def should_send_error_email(self) -> bool:
        return self.error and not self.error_email_sent

    def send_error_email(self):
        self.mail_error_to_admins()
        self.mark_error_email_as_sent()

    def mail_error_to_admins(self):
        email_manager.send_emails(
            emails=[email for _, email in settings.ADMINS],
            template_name="client_log_error",
            subject=_("Error in {} API Client").format(self.client_code),
            context={
                "error": self.error,
                "client_code": self.client_code,
                "method": self.get_method_display(),
                "url": self.url,
            },
        )

    def mark_error_email_as_sent(self):
        self.error_email_sent = True
        self.save()

    def to_dict(self):
        return {
            "method": self.method,
            "url": self.url,
            "client_code": self.client_code,
            "request_time": self.request_time,
            "request_headers": self.request_headers,
            "request_content": self.request_content,
            "response_time": self.response_time,
            "response_headers": self.response_headers,
            "response_content": self.response_content,
            "response_status_code": self.response_status_code,
        }
