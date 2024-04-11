from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TimeFrameChoices(TextChoices):
    DAILY = "DAILY", _("Daily")
    WEEKLY = "WEEKLY", _("Weekly")
    MONTHLY = "MONTHLY", _("Monthly")
    QUARTERLY = "QUARTERLY", _("Quarterly")
    SEMIANNUALLY = "SEMIANNUALLY", _("Semiannually")
    ANNUALLY = "ANNUALLY", _("Annually")
