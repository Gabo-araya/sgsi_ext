from django.contrib import admin

from api_client.models import ClientLog


@admin.register(ClientLog)
class ClientLogAdmin(admin.ModelAdmin):
    pass
