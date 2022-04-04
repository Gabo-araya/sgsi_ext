# django
from django.db.models.enums import TextChoices
from django.utils.translation import ugettext_lazy as _


class ParameterKind(TextChoices):
    """Represents the available choices of parameter kinds"""

    INT = ("int", _("integer"))
    STR = ("str", _("text"))
    TIME = ("time", _("time"))
    DATE = ("date", _("date"))
    JSON = ("json", _("json"))
    BOOL = ("bool", _("boolean"))  # 'true', '1' or 'yes'
