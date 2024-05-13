from base.views.generic import BaseCreateView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from base.views.generic.edit import BaseUpdateRedirectView
from information_assets.forms import AssetForm
from information_assets.managers import AssetQuerySet
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

    def get_queryset(self) -> AssetQuerySet:
        return super().get_queryset().not_archived()


class AssetToggleArchiveView(BaseUpdateRedirectView):
    model = Asset
    permission_required = "information_assets.archive_asset"

    def do_action(self):
        self.object.toggle_archive()

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get(
            "HTTP_REFERER", super().get_redirect_url(*args, **kwargs)
        )
