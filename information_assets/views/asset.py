from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from information_assets.forms import AssetForm
from information_assets.models.asset import Asset


class AssetListView(BaseListView):
    model = Asset
    template_name = "information_assets/asset/list.html"
    permission_required = "information_assets.view_asset"


class AssetCreateView(BaseCreateView):
    model = Asset
    form_class = AssetForm
    template_name = "information_assets/asset/create.html"
    permission_required = "information_assets.add_asset"


class AssetDetailView(BaseDetailView):
    model = Asset
    template_name = "information_assets/asset/detail.html"
    permission_required = "information_assets.view_asset"


class AssetUpdateView(BaseUpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "information_assets/asset/update.html"
    permission_required = "information_assets.change_asset"


class AssetDeleteView(BaseDeleteView):
    model = Asset
    template_name = "information_assets/asset/delete.html"
    permission_required = "information_assets.delete_asset"
