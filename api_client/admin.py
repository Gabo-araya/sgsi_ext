import ast

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from api_client.models import ClientLog


@admin.register(ClientLog)
class ClientLogAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    search_fields = ["url", "client_code", "endpoint"]
    list_display = [
        "created_at",
        "client_code",
        "method",
        "url",
        "response_status_code",
    ]
    list_filter = ["client_code"]
    fieldsets = (
        (
            "Metadata",
            {
                "fields": (
                    "client_code",
                    "created_at",
                    "updated_at",
                    "error",
                    "method",
                    "url",
                )
            },
        ),
        (
            "Request",
            {
                "fields": (
                    "request_time",
                    "request_headers_pretty",
                    "request_content_pretty",
                )
            },
        ),
        (
            "Response",
            {
                "fields": (
                    "response_time",
                    "response_headers_pretty",
                    "response_content_pretty",
                    "response_status_code",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_("request headers").capitalize())
    def request_headers_pretty(self, obj):
        return self._format_headers(obj, "request_headers")

    @admin.display(description=_("response headers").capitalize())
    def response_headers_pretty(self, obj):
        return self._format_headers(obj, "response_headers")

    @admin.display(description=_("request content").capitalize())
    def request_content_pretty(self, obj):
        return self._format_body(obj, "request_content")

    @admin.display(description=_("response content").capitalize())
    def response_content_pretty(self, obj):
        return self._format_body(obj, "response_content")

    def _format_headers(self, obj, field):
        value = getattr(obj, field)
        try:
            # request and response fields do not contain a JSON representation but a
            # str() representation of the original dictionary
            parsed_headers = ast.literal_eval(value)
            formatted_headers = (
                f"{key}: {value}" for key, value in parsed_headers.items()
            )
            return format_html("<pre>{}</pre>", "\n".join(formatted_headers))
        except (ValueError, SyntaxError):
            return format_html("<pre>{}</pre>", value)

    def _format_body(self, obj, field):
        value = getattr(obj, field)
        return format_html("<pre>{}</pre>", value)
