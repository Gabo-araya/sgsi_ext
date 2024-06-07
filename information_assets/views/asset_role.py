from typing import Any

from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from information_assets.forms import AssetRoleChangeForm
from information_assets.forms import AssetRoleForm
from information_assets.models.asset import Asset
from information_assets.models.asset_role import AssetRole


class RoleListView(BaseListView):
    model = AssetRole
    template_name = "information_assets/assetrole/list.html"
    permission_required = "information_assets.view_assetrole"


class RoleCreateView(BaseCreateView):
    model = AssetRole
    form_class = AssetRoleForm
    template_name = "information_assets/assetrole/create.html"
    permission_required = "information_assets.add_assetrole"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        asset_pk = self.request.GET.get("asset_pk")
        asset = Asset.objects.filter(pk=asset_pk).first()
        if asset is not None:
            initial["asset"] = asset
        return initial


class RoleDetailView(BaseDetailView):
    model = AssetRole
    template_name = "information_assets/assetrole/detail.html"
    permission_required = "information_assets.view_assetrole"


class RoleUpdateView(BaseUpdateView):
    model = AssetRole
    form_class = AssetRoleChangeForm
    template_name = "information_assets/assetrole/update.html"
    permission_required = "information_assets.change_assetrole"


class RoleDeleteView(BaseDeleteView):
    model = AssetRole
    permission_required = "information_assets.delete_assetrole"
    template_name = "information_assets/assetrole/delete.html"
