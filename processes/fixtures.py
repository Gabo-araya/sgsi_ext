import pytest

from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance


@pytest.fixture
@pytest.mark.django_db
def process(control):
    return Process.objects.create(
        name="test process",
        control=control,
    )


@pytest.fixture
@pytest.mark.django_db
def process_activity(process, regular_user):
    return ProcessActivity.objects.create(
        process=process,
        description="test description",
        asignee=regular_user,
    )


@pytest.fixture
@pytest.mark.django_db
def process_instance(process):
    return ProcessInstance.objects.create(
        process=process,
    )


@pytest.fixture
@pytest.mark.django_db
def process_activity_instance(process_instance, process_activity):
    return ProcessActivityInstance.objects.create(
        process_instance=process_instance,
        activity=process_activity,
        order=process_activity.order,
        description=process_activity.description,
        asignee=process_activity.asignee,
    )
