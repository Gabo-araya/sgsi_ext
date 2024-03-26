from django.db.models import QuerySet


class DocumentVersionQuerySet(QuerySet):
    def approved(self):
        return self.filter(is_approved=True)

    def not_approved(self):
        return self.filter(is_approved=False)
