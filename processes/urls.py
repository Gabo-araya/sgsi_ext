from django.urls import include
from django.urls import path

from processes.views import process_activity as processactivity_views
from processes.views import process_activity_instance as processactivityinstance_views
from processes.views import process_instance as processinstance_views
from processes.views import process_version as processversion_views

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

processversion_urlpatterns = [
    path(
        "",
        processversion_views.ProcessVersionListView.as_view(),
        name="processversion_list",
    ),
    path(
        "create/",
        processversion_views.ProcessVersionCreateView.as_view(),
        name="processversion_create",
    ),
    path(
        "<int:pk>/",
        processversion_views.ProcessVersionDetailView.as_view(),
        name="processversion_detail",
    ),
    path(
        "<int:pk>/update/",
        processversion_views.ProcessVersionUpdateView.as_view(),
        name="processversion_update",
    ),
    path(
        "<int:pk>/delete/",
        processversion_views.ProcessVersionDeleteView.as_view(),
        name="processversion_delete",
    ),
    path(
        "<int:parent_pk>/activities/create/",
        processactivity_views.ProcessActivityCreateView.as_view(),
        name="processactivity_create",
    ),
]

processactivityinstance_urlpatterns = [
    path(
        "<int:pk>/complete/",
        processactivityinstance_views.ProcessActivityInstanceCompleteView.as_view(),
        name="processactivityinstance_complete",
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
    path("process-instances/", include(processinstance_urlpatterns)),
    path("process-versions/", include(processversion_urlpatterns)),
    path("activity-instances/", include(processactivityinstance_urlpatterns)),
    path("activities/", include(processactivity_urlpatterns)),
]
