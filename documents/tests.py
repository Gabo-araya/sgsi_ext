from django.db import IntegrityError

import pytest

from pytest_lazyfixture import lazy_fixture

from documents.models.evidence import Evidence

INTEGRITY_ERROR_MSG = (
    'new row for relation "documents_evidence" violates check constraint '
    '"file_url_or_text"'
)


@pytest.mark.django_db
def test_evidence_file_url_or_text(django_file):
    Evidence.objects.create(file=django_file)
    Evidence.objects.create(url="https://example.com")
    Evidence.objects.create(text="Some text")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "file, url, text",
    (
        (
            lazy_fixture("django_file"),
            "https://example.com",
            "Some text",
        ),
        (
            lazy_fixture("django_file"),
            "https://example.com",
            None,
        ),
        (
            lazy_fixture("django_file"),
            None,
            "Some text",
        ),
        (
            None,
            "https://example.com",
            "Some text",
        ),
    ),
)
def test_evidence_file_url_or_text_violation_raises(file, url, text):
    evidence_kwargs = {}
    for key, value in (("file", file), ("url", url), ("text", text)):
        if value is not None:
            evidence_kwargs[key] = value
    with pytest.raises(IntegrityError, match=INTEGRITY_ERROR_MSG):
        Evidence.objects.create(**evidence_kwargs)


@pytest.mark.django_db
def test_evidence_no_file_nor_url_nor_text_raises():
    with pytest.raises(IntegrityError, match=INTEGRITY_ERROR_MSG):
        Evidence.objects.create()
