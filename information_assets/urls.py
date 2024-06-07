from django.urls import include
from django.urls import path

from information_assets.views import asset as asset_views
from information_assets.views import asset_role as assetrole_views
from information_assets.views import asset_type as assettype_views

assert_urlpatterns = [
    path(
        "",
        asset_views.AssetListView.as_view(),
        name="asset_list",
    ),
    path(
        "create/",
        asset_views.AssetCreateView.as_view(),
        name="asset_create",
    ),
    path(
        "<int:pk>/",
        asset_views.AssetDetailView.as_view(),
        name="asset_detail",
    ),
    path(
        "<int:pk>/update/",
        asset_views.AssetUpdateView.as_view(),
        name="asset_update",
    ),
    path(
        "<int:pk>/toggle-archive/",
        asset_views.AssetToggleArchiveView.as_view(),
        name="asset_toggle_archive",
    ),
]

assettype_urlpatterns = [
    path(
        "",
        assettype_views.AssetTypeListView.as_view(),
        name="assettype_list",
    ),
    path(
        "create/",
        assettype_views.AssetTypeCreateView.as_view(),
        name="assettype_create",
    ),
    path(
        "<int:pk>/",
        assettype_views.AssetTypeDetailView.as_view(),
        name="assettype_detail",
    ),
    path(
        "<int:pk>/update/",
        assettype_views.AssetTypeUpdateView.as_view(),
        name="assettype_update",
    ),
    path(
        "<int:pk>/delete/",
        assettype_views.AssetTypeDeleteView.as_view(),
        name="assettype_delete",
    ),
]

assetrole_urlpatterns = [
    path(
        "",
        assetrole_views.RoleListView.as_view(),
        name="assetrole_list",
    ),
    path(
        "create/",
        assetrole_views.RoleCreateView.as_view(),
        name="assetrole_create",
    ),
    path(
        "<int:pk>/",
        assetrole_views.RoleDetailView.as_view(),
        name="assetrole_detail",
    ),
    path(
        "<int:pk>/update/",
        assetrole_views.RoleUpdateView.as_view(),
        name="assetrole_update",
    ),
    path(
        "<int:pk>/delete/",
        assetrole_views.RoleDeleteView.as_view(),
        name="assetrole_delete",
    ),
]

urlpatterns = [
    path("assets/", include(assert_urlpatterns)),
    path("assets-roles/", include(assetrole_urlpatterns)),
    path("asset-types/", include(assettype_urlpatterns)),
]
