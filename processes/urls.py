from django.urls import include
from django.urls import path

from processes.views import process as process_views
from processes.views import process_activity as processactivity_views
from processes.views import (
    process_activity_instance as processactivityinstanceinstance_views,
)
from processes.views import process_definition as processdefinition_views

process_urlpatterns = [
    path(
        "",
        process_views.ProcessListView.as_view(),
        name="process_list",
    ),
    path(
        "create/",
        process_views.ProcessCreateView.as_view(),
        name="process_create",
    ),
    path(
        "<int:pk>/",
        process_views.ProcessDetailView.as_view(),
        name="process_detail",
    ),
    path(
        "<int:pk>/update/",
        process_views.ProcessUpdateView.as_view(),
        name="process_update",
    ),
    path(
        "<int:pk>/delete/",
        process_views.ProcessDeleteView.as_view(),
        name="process_delete",
    ),
]

processdefinition_urlpatterns = [
    path(
        "",
        processdefinition_views.ProcessDefinitionListView.as_view(),
        name="processdefinition_list",
    ),
    path(
        "create/",
        processdefinition_views.ProcessDefinitionCreateView.as_view(),
        name="processdefinition_create",
    ),
    path(
        "<int:pk>/",
        processdefinition_views.ProcessDefinitionDetailView.as_view(),
        name="processdefinition_detail",
    ),
    path(
        "<int:pk>/update/",
        processdefinition_views.ProcessDefinitionUpdateView.as_view(),
        name="processdefinition_update",
    ),
    path(
        "<int:pk>/delete/",
        processdefinition_views.ProcessDefinitionDeleteView.as_view(),
        name="processdefinition_delete",
    ),
    path(
        "<int:parent_pk>/activities/create/",
        processactivity_views.ProcessActivityCreateView.as_view(),
        name="processactivity_create",
    ),
]

processactivityinstanceinstance_urlpatterns = [
    path(
        "<int:pk>/complete/",
        processactivityinstanceinstance_views.ProcessActivityInstanceCompleteView.as_view(),
        name="processactivityinstanceinstance_complete",
    )
]

processactivity_urlpatterns = [
    path(
        "<int:pk>/",
        processactivity_views.ProcessActivityDetailView.as_view(),
        name="processactivity_detail",
    ),
    path(
        "<int:pk>/update/",
        processactivity_views.ProcessActivityUpdateView.as_view(),
        name="processactivity_update",
    ),
    path(
        "<int:pk>/delete/",
        processactivity_views.ProcessActivityDeleteView.as_view(),
        name="processactivity_delete",
    ),
]

urlpatterns = [
    path("processes/", include(process_urlpatterns)),
    path("process-definitions/", include(processdefinition_urlpatterns)),
    path("activity-instances/", include(processactivityinstanceinstance_urlpatterns)),
    path("activities/", include(processactivity_urlpatterns)),
]
