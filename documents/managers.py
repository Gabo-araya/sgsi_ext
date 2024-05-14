from __future__ import annotations

from django.db import models
from django.db.models import QuerySet

from typing_extensions import Self

from documents.models.document_version_read_by_user import DocumentVersionReadByUser
from users.models.user import User


class DocumentVersionQuerySet(QuerySet):
    def approved(self) -> Self:
        return self.filter(is_approved=True)

    def not_approved(self) -> Self:
        return self.filter(is_approved=False)

    def evidences(self) -> Self:
        from documents.models.evidence import Evidence

        return Evidence.objects.filter(document_version__in=self)

    def annotate_is_read_by_user(self, user: User) -> Self:
        return self.annotate(
            is_read_by_user=models.Exists(
                DocumentVersionReadByUser.objects.filter(
                    document_version=models.OuterRef("pk"), user=user
                )
            )
        )
