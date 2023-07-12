""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""

import datetime
import decimal
import uuid

from json import JSONEncoder

from django.core.files.uploadedfile import UploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile
from django.utils.duration import duration_iso_string
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.timezone import is_aware


class ModelEncoder(DjangoJSONEncoder):
    def default(self, obj):
        from base.models import BaseModel

        if isinstance(obj, FieldFile):
            return obj.url if obj else None

        if isinstance(obj, UploadedFile):
            return f"<Unsaved file: {obj.name}>"

        if isinstance(obj, BaseModel):
            return obj.to_dict()

        if isinstance(obj, decimal.Decimal):
            return str(obj)

        if isinstance(obj, Promise):
            return force_str(obj)

        return super().default(obj)


class StringFallbackJSONEncoder(JSONEncoder):
    """JSON Serializer that falls back to force_str."""

    def default(self, obj):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(obj, datetime.datetime):
            return self.process_datetime(obj)
        if isinstance(obj, datetime.date):
            return self.process_date(obj)
        if isinstance(obj, datetime.time):
            return self.process_time(obj)
        if isinstance(obj, datetime.timedelta):
            return self.process_timedelta(obj)
        if isinstance(obj, (decimal.Decimal, uuid.UUID, Promise)):
            return self.process_decimal_uuid_or_promise(obj)
        return self.process_other(obj)

    def process_other(self, obj):
        # dict-like classes that don't descend from `dict` are handled with duck typing
        if hasattr(obj, "__getitem__") and not isinstance(obj, bytes):
            cls = list if isinstance(obj, (list, tuple)) else dict
            try:
                return cls(obj)
            except ValueError:
                return self.process_other(obj)
        try:
            return force_str(obj)
        except DjangoUnicodeDecodeError:
            return super().default(obj)

    def process_decimal_uuid_or_promise(self, obj):
        return str(obj)

    def process_timedelta(self, obj):
        return duration_iso_string(obj)

    def process_time(self, obj):
        if is_aware(obj):
            msg = "JSON can't represent timezone-aware times."
            raise ValueError(msg)
        iso = obj.isoformat()
        if obj.microsecond:
            return iso[:12]
        return iso

    def process_date(self, obj):
        return obj.isoformat()

    def process_datetime(self, obj):
        iso = obj.isoformat()
        if obj.microsecond:
            iso = iso[:23] + iso[26:]
        if iso.endswith("+00:00"):
            iso = iso[:-6] + "Z"
        return iso
