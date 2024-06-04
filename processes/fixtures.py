import pytest

from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance
from processes.models.process_version import ProcessVersion


@pytest.fixture
@pytest.mark.django_db
def process():
    return Process.objects.create(
        name="test process",
    )


@pytest.fixture
@pytest.mark.django_db
def process_version(process, document, control):
    process_version = ProcessVersion.objects.create(
        process=process,
        defined_in=document,
    )
    process_version.controls.set([control])
    return process_version


@pytest.fixture
@pytest.mark.django_db
def process_activity(process_version, group):
    process_activity = ProcessActivity.objects.create(
        process_version=process_version,
        description="test description",
    )
    process_activity.assignee_groups.set([group])
    return process_activity


@pytest.fixture
@pytest.mark.django_db
def process_instance(process_version, regular_user):
    return ProcessInstance.objects.create(
        process_version=process_version,
        created_by=regular_user,
    )


@pytest.fixture
@pytest.mark.django_db
def process_activity_instance(process_instance, process_activity, superuser_user):
    return ProcessActivityInstance.objects.create(
        process_instance=process_instance,
        activity=process_activity,
        assignee=superuser_user,
    )
