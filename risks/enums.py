from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class LikelihoodChoices(TextChoices):
    VERY_LOW = "VERY_LOW", _("Very Low")
    LOW = "LOW", _("Low")
    MEDIUM = "MEDIUM", _("Medium")
    HIGH = "HIGH", _("High")
    VERY_HIGH = "VERY_HIGH", _("Very High")


class SeverityChoices(TextChoices):
    VERY_LOW = "VERY_LOW", _("Very Low")
    LOW = "LOW", _("Low")
    MEDIUM = "MEDIUM", _("Medium")
    HIGH = "HIGH", _("High")
    VERY_HIGH = "VERY_HIGH", _("Very High")


class TreatmentChoices(TextChoices):
    MITIGATE = "MITIGATE", _("Mitigate")
    TRANSFER = "TRANSFER", _("Transfer")
    ACCEPT = "ACCEPT", _("Accept")
    ELIMINATE = "ELIMINATE", _("Eliminate")
