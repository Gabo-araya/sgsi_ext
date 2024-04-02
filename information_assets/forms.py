from base.forms import BaseModelForm
from information_assets.models.asset import Asset
from information_assets.models.asset_type import AssetType


class AssetForm(BaseModelForm):
    class Meta:
        model = Asset
        fields = (
            "name",
            "owner",
            "description",
            "asset_type",
            "criticality",
            "classification",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "owner"
        ].label_from_instance = lambda user: user.get_label_for_instance()


class AssetTypeForm(BaseModelForm):
    class Meta:
        model = AssetType
        fields = (
            "name",
            "description",
        )
