from django.urls import path

from .views import views

urlpatterns = [
    path(
        "",
        views.RiskListView.as_view(),
        name="risk_list",
    ),
    path(
        "create/",
        views.RiskCreateView.as_view(),
        name="risk_create",
    ),
    path(
        "<int:pk>/",
        views.RiskDetailView.as_view(),
        name="risk_detail",
    ),
    path(
        "<int:pk>/update/",
        views.RiskUpdateView.as_view(),
        name="risk_update",
    ),
    path(
        "<int:pk>/delete/",
        views.RiskDeleteView.as_view(),
        name="risk_delete",
    ),
]
