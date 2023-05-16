from django.db import models
from django.utils.translation import gettext_lazy as _


class ClientLog(models.Model):
    class MethodOptions(models.TextChoices):
        GET = "GET", _("GET")
        POST = "POST", _("POST")
        PUT = "PUT", _("PUT")
        PATCH = "PATCH", _("PATCH")
        DELETE = "DELETE", _("DELETE")

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
    request_headers = models.TextField(
        verbose_name=_("headers"),
    )
    request_content = models.TextField(
        verbose_name=_("content"),
    )
    request_error = models.TextField(
        verbose_name=_("error"),
    )
    response_headers = models.TextField(
        verbose_name=_("headers"),
    )
    response_content = models.TextField(
        verbose_name=_("content"),
    )
    response_error = models.TextField(
        verbose_name=_("error"),
    )
    response_status_code = models.IntegerField(
        verbose_name=_("status code"),
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.method.upper()} {self.url}"
