from django.db import models


class ProcessVersionQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def not_published(self):
        return self.filter(is_published=False)
