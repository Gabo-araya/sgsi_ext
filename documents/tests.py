from django.db import IntegrityError

import pytest

from documents.models.evidence import Evidence

INTEGRITY_ERROR_MSG = (
    'new row for relation "documents_evidence" violates check constraint '
    '"file_xor_url"'
)


@pytest.mark.django_db
def test_evidence_file_xor_url(django_file):
    Evidence.objects.create(file=django_file)
    Evidence.objects.create(url="https://example.com")


@pytest.mark.django_db
def test_evidence_file_and_url_raises(django_file):
    with pytest.raises(IntegrityError, match=INTEGRITY_ERROR_MSG):
        Evidence.objects.create(file=django_file, url="https://example.com")


@pytest.mark.django_db
def test_evidence_no_file_nor_url_raises():
    with pytest.raises(IntegrityError, match=INTEGRITY_ERROR_MSG):
        Evidence.objects.create()
