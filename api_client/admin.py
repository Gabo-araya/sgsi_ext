from django.contrib import admin

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
                    "request_headers",
                    "request_content",
                )
            },
        ),
        (
            "Response",
            {
                "fields": (
                    "response_time",
                    "response_headers",
                    "response_content",
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
