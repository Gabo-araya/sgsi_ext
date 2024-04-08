from django.contrib import admin

from information_assets.models.asset import Asset
from information_assets.models.asset_type import AssetType


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    pass
