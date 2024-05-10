from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from users.models.user import User


class ProcessQuerySet(models.QuerySet):
    def instantiable_by_user(self, user: User):
        return self.filter(
            versions__is_published=True,
            versions__activities__order=1,
            versions__activities__assignee_group__user=user,
        ).distinct()


class ProcessVersionQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def not_published(self):
        return self.filter(is_published=False)


class ProcessInstanceQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(is_completed=True)

    def not_completed(self):
        return self.filter(is_completed=False)

    def user_is_participant(self, user: User):
        return self.filter(activity_instances__assignee=user).distinct()


class ProcessActivityInstanceQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(is_completed=True)

    def not_completed(self):
        return self.filter(is_completed=False)
