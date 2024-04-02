from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CriticalityChoices(TextChoices):
    VERY_LOW = "VERY_LOW", _("Very low")
    LOW = "LOW", _("Low")
    MEDIUM = "MEDIUM", _("Medium")
    HIGH = "HIGH", _("High")
    VERY_HIGH = "VERY_HIGH", _("Very high")


class ClassificationChoices(TextChoices):
    PUBLIC = "PUBLIC", _("Public")
    INTERNAL = "INTERNAL", _("Internal")
    PRIVATE = "PRIVATE", _("Private")
