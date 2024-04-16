from __future__ import annotations

from django.db.models import QuerySet


class DocumentVersionQuerySet(QuerySet):
    def approved(self):
        return self.filter(is_approved=True)

    def not_approved(self):
        return self.filter(is_approved=False)

    def evidences(self):
        from documents.models.evidence import Evidence

        return Evidence.objects.filter(document_version__in=self)
