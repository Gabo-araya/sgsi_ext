from django.db import models


class AssetQuerySet(models.QuerySet):
    def archived(self):
        return self.filter(is_archived=True)

    def not_archived(self):
        return self.filter(is_archived=False)
