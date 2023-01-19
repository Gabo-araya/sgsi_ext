""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""

# standard library
import datetime
import decimal
import uuid

from json import JSONEncoder

# django
from django.core.files.uploadedfile import UploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile
from django.utils.duration import duration_iso_string
from django.utils.encoding import force_str
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.utils.timezone import is_aware


class ModelEncoder(DjangoJSONEncoder):
    def default(self, obj):
        from base.models import BaseModel

        if isinstance(obj, FieldFile):
            if obj:
                return obj.url
            else:
                return None

        elif isinstance(obj, UploadedFile):
            return f"<Unsaved file: {obj.name}>"

        elif isinstance(obj, BaseModel):
            return obj.to_dict()

        elif isinstance(obj, decimal.Decimal):
            return str(obj)

        elif isinstance(obj, Promise):
            return force_text(obj)

        return super(ModelEncoder, self).default(obj)


class StringFallbackJSONEncoder(JSONEncoder):
    """JSON Serializer that falls back to force_str."""

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r[:-6] + "Z"
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
            return str(o)
        else:
            try:
                return force_str(o)
            except Exception:
                return super().default(o)
