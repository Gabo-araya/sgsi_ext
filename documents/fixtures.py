import pytest

from documents.models.control import Control
from documents.models.control_category import ControlCategory
from documents.models.document import Document
from documents.models.document_read_by_user import DocumentReadByUser
from documents.models.document_version import DocumentVersion


@pytest.fixture
@pytest.mark.django_db
def control_category():
    return ControlCategory.objects.create(name="test control")


@pytest.fixture
@pytest.mark.django_db
def control(control_category, document):
    return Control.objects.create(
        category=control_category,
        title="test control",
        description="test description",
        document=document,
    )


@pytest.fixture
@pytest.mark.django_db
def document_read_by_user(document_version, regular_user):
    return DocumentReadByUser.objects.create(
        document_version=document_version,
        user=regular_user,
    )


@pytest.fixture
@pytest.mark.django_db
def document_version(document, django_file):
    return DocumentVersion.objects.create(document=document, file=django_file)


@pytest.fixture
@pytest.mark.django_db
def document():
    return Document.objects.create(
        title="test document", description="test description"
    )
