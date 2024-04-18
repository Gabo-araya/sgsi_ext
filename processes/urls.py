from django.urls import include
from django.urls import path

from processes.views import process_activity as processactivity_views
from processes.views import (
    process_activity_instance as processactivityinstanceinstance_views,
)
from processes.views import process_definition as processdefinition_views
from processes.views import process_instance as processinstance_views

processinstance_urlpatterns = [
    path(
        "",
        processinstance_views.ProcessInstanceListView.as_view(),
        name="processinstance_list",
    ),
    path(
        "create/",
        processinstance_views.ProcessInstanceCreateView.as_view(),
        name="processinstance_create",
    ),
    path(
        "<int:pk>/",
        processinstance_views.ProcessInstanceDetailView.as_view(),
        name="processinstance_detail",
    ),
    path(
        "<int:pk>/update/",
        processinstance_views.ProcessInstanceUpdateView.as_view(),
        name="processinstance_update",
    ),
    path(
        "<int:pk>/delete/",
        processinstance_views.ProcessInstanceDeleteView.as_view(),
        name="processinstance_delete",
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
    path("processes/", include(processinstance_urlpatterns)),
    path("process-definitions/", include(processdefinition_urlpatterns)),
    path("activity-instances/", include(processactivityinstanceinstance_urlpatterns)),
    path("activities/", include(processactivity_urlpatterns)),
]
