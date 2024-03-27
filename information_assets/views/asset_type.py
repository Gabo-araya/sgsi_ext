from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from information_assets.forms import AssetTypeForm
from information_assets.models.asset_type import AssetType


class AssetTypeListView(BaseListView):
    model = AssetType
    template_name = "information_assets/asset_type/list.html"
    permission_required = "information_assets.view_assettype"


class AssetTypeCreateView(BaseCreateView):
    model = AssetType
    form_class = AssetTypeForm
    template_name = "information_assets/asset_type/create.html"
    permission_required = "information_assets.add_assettype"


class AssetTypeDetailView(BaseDetailView):
    model = AssetType
    template_name = "information_assets/asset_type/detail.html"
    permission_required = "information_assets.view_assettype"


class AssetTypeUpdateView(BaseUpdateView):
    model = AssetType
    form_class = AssetTypeForm
    template_name = "information_assets/asset_type/update.html"
    permission_required = "information_assets.change_assettype"


class AssetTypeDeleteView(BaseDeleteView):
    model = AssetType
    template_name = "information_assets/asset_type/delete.html"
    permission_required = "information_assets.delete_assettype"
