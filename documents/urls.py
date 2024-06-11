from django.urls import include
from django.urls import path

from documents.views import control as control_views
from documents.views import control_category as controlcategory_views
from documents.views import document as document_views
from documents.views import document_type as documenttype_views
from documents.views import document_version as documentversion_views
from documents.views import evidence as evidence_views

document_urlpatterns = [
    path(
        "",
        document_views.DocumentListView.as_view(),
        name="document_list",
    ),
    path(
        "create/",
        document_views.DocumentCreateView.as_view(),
        name="document_create",
    ),
    path(
        "<slug:slug>/",
        document_views.DocumentDetailView.as_view(),
        name="document_detail",
    ),
    path(
        "<slug:slug>/update/",
        document_views.DocumentUpdateView.as_view(),
        name="document_update",
    ),
    path(
        "<slug:slug>/delete/",
        document_views.DocumentDeleteView.as_view(),
        name="document_delete",
    ),
]

documentversion_urlpatterns = [
    path(
        "<slug:parent_slug>/versions/create/",
        documentversion_views.DocumentVersionCreateView.as_view(),
        name="documentversion_create",
    ),
    path(
        "<slug:document_code>/V<int:version>/",
        documentversion_views.DocumentVersionDetailView.as_view(),
        name="documentversion_detail",
    ),
    path(
        "<slug:document_code>/V<int:version>/update/",
        documentversion_views.DocumentVersionUpdateView.as_view(),
        name="documentversion_update",
    ),
    path(
        "<slug:document_code>/V<int:version>/delete/",
        documentversion_views.DocumentVersionDeleteView.as_view(),
        name="documentversion_delete",
    ),
    path(
        "<slug:document_code>/V<int:version>/approve/",
        documentversion_views.DocumentVersionApproveView.as_view(),
        name="documentversion_approve",
    ),
    path(
        "<slug:document_code>/V<int:version>/mark-as-read/",
        documentversion_views.DocumentVersionMarkAsReadView.as_view(),
        name="documentversion_mark_as_read",
    ),
]

controlcatergory_urlpatterns = [
    path(
        "",
        controlcategory_views.ControlCategoryListView.as_view(),
        name="controlcategory_list",
    ),
    path(
        "create/",
        controlcategory_views.ControlCategoryCreateView.as_view(),
        name="controlcategory_create",
    ),
    path(
        "<int:pk>/",
        controlcategory_views.ControlCategoryDetailView.as_view(),
        name="controlcategory_detail",
    ),
    path(
        "<int:pk>/update/",
        controlcategory_views.ControlCategoryUpdateView.as_view(),
        name="controlcategory_update",
    ),
    path(
        "<int:pk>/delete/",
        controlcategory_views.ControlCategoryDeleteView.as_view(),
        name="controlcategory_delete",
    ),
]

control_urlpatterns = [
    path(
        "",
        control_views.ControlListView.as_view(),
        name="control_list",
    ),
    path(
        "create/",
        control_views.ControlCreateView.as_view(),
        name="control_create",
    ),
    path(
        "<int:pk>/",
        control_views.ControlDetailView.as_view(),
        name="control_detail",
    ),
    path(
        "<int:pk>/update/",
        control_views.ControlUpdateView.as_view(),
        name="control_update",
    ),
    path(
        "<int:pk>/delete/",
        control_views.ControlDeleteView.as_view(),
        name="control_delete",
    ),
]

evidence_urlpatterns = [
    path(
        "<int:pk>/",
        evidence_views.EvidenceDetailView.as_view(),
        name="evidence_detail",
    )
]

documenttype_urlpatterns = [
    path(
        "",
        documenttype_views.DocumentTypeListView.as_view(),
        name="documenttype_list",
    ),
    path(
        "create/",
        documenttype_views.DocumentTypeCreateView.as_view(),
        name="documenttype_create",
    ),
    path(
        "<int:pk>/",
        documenttype_views.DocumentTypeDetailView.as_view(),
        name="documenttype_detail",
    ),
    path(
        "<int:pk>/update/",
        documenttype_views.DocumentTypeUpdateView.as_view(),
        name="documenttype_update",
    ),
    path(
        "<int:pk>/delete/",
        documenttype_views.DocumentTypeDeleteView.as_view(),
        name="documenttype_delete",
    ),
]


urlpatterns = [
    path("documents/", include(document_urlpatterns)),
    path("documents/", include(documentversion_urlpatterns)),
    path("document-types/", include(documenttype_urlpatterns)),
    path("controls/", include(control_urlpatterns)),
    path("control-categories/", include(controlcatergory_urlpatterns)),
    path("evidences/", include(evidence_urlpatterns)),
]
