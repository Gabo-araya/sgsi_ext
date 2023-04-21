# standard library
import json

# django
from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import CHANGE
from django.contrib.admin.models import DELETION
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str

# base
from base.serializers import ModelEncoder


class AuditMixin:
    """
    Mixin that gives to BaseModel the function needed to create
    the EntryLogs.
    """

    def _save_log(self, user, message, action):
        if not user or not user.id:
            return

        LogEntry.objects.create(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(self).id,
            object_id=self.id,
            object_repr=force_str(self)[:200],
            action_flag=action,
            change_message=json.dumps(message, cls=ModelEncoder),
        )

    def _save_addition(self, user, message):
        self._save_log(user, message, ADDITION)

    def _save_edition(self, user, message):
        self._save_log(user, message, CHANGE)

    def _save_deletion(self, user):
        self._save_log(user, {"Deleted": None}, DELETION)
