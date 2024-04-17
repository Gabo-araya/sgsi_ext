from django.urls import include
from django.urls import path

from processes.views import process as process_views
from processes.views import (
    process_activity_definition as processactivitydefinition_views,
)
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
        "<int:parent_pk>/activity-definitions/create/",
        processactivitydefinition_views.ProcessActivityDefinitionCreateView.as_view(),
        name="processactivitydefinition_create",
    ),
]

processactivityinstanceinstance_urlpatterns = [
    path(
        "<int:pk>/complete/",
        processactivityinstanceinstance_views.ProcessActivityInstanceCompleteView.as_view(),
        name="processactivityinstanceinstance_complete",
    )
]

processactivitydefinition_urlpatterns = [
    path(
        "<int:pk>/",
        processactivitydefinition_views.ProcessActivityDefinitionDetailView.as_view(),
        name="processactivitydefinition_detail",
    ),
    path(
        "<int:pk>/update/",
        processactivitydefinition_views.ProcessActivityDefinitionUpdateView.as_view(),
        name="processactivitydefinition_update",
    ),
    path(
        "<int:pk>/delete/",
        processactivitydefinition_views.ProcessActivityDefinitionDeleteView.as_view(),
        name="processactivitydefinition_delete",
    ),
]

urlpatterns = [
    path("processes/", include(process_urlpatterns)),
    path("process-definitions/", include(processdefinition_urlpatterns)),
    path("activities/", include(processactivityinstanceinstance_urlpatterns)),
    path("activity-definitions/", include(processactivitydefinition_urlpatterns)),
]
