from django.db import models
from django.utils.translation import gettext_lazy as _


class ClientCodes(models.TextChoices):
    DUMMY_INTEGRATION = "DUMMY_INTEGRATION", _("Dummy Integration")
