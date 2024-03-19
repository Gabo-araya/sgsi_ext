from django.urls import path

from documents import views

urlpatterns = [
    path(
        "",
        views.DocumentListView.as_view(),
        name="document_list",
    ),
    path(
        "create/",
        views.DocumentCreateView.as_view(),
        name="document_create",
    ),
    path(
        "<int:pk>/",
        views.DocumentDetailView.as_view(),
        name="document_detail",
    ),
    path(
        "<int:pk>/update/",
        views.DocumentUpdateView.as_view(),
        name="document_update",
    ),
    path(
        "<int:pk>/delete/",
        views.DocumentDeleteView.as_view(),
        name="document_delete",
    ),
]
