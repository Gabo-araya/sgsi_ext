from django.contrib import admin

from information_assets.models.asset import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass
