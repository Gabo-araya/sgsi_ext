from django.urls import path

from risks.views import risk as risk_views

urlpatterns = [
    path(
        "",
        risk_views.RiskListView.as_view(),
        name="risk_list",
    ),
    path(
        "create/",
        risk_views.RiskCreateView.as_view(),
        name="risk_create",
    ),
    path(
        "<int:pk>/",
        risk_views.RiskDetailView.as_view(),
        name="risk_detail",
    ),
    path(
        "<int:pk>/update/",
        risk_views.RiskUpdateView.as_view(),
        name="risk_update",
    ),
    path(
        "<int:pk>/delete/",
        risk_views.RiskDeleteView.as_view(),
        name="risk_delete",
    ),
]
