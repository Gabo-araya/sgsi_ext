from django.db import models
from django.utils.translation import gettext_lazy as _


class ClientCodes(models.TextChoices):
    """
    Client codes for API clients.

    All clients must have a unique code that should be declared here.
    """

    DUMMY_INTEGRATION = "DUMMY_INTEGRATION", _("Dummy Integration")
