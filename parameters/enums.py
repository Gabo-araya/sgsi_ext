# django
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _


class ParameterKind(TextChoices):
    """Represents the available choices of parameter kinds"""

    INT = ("int", _("integer"))
    TIME = ("time", _("time"))
    DATE = ("date", _("date"))
    JSON = ("json", _("json"))
    URL = ("url", _("url"))
    HOSTNAME = ("host", _("host name"))
    IP_NETWORK = ("ip_net", _("IP prefix/range"))
    HOSTNAME_LIST = ("host_list", _("host name list"))
    IP_NETWORK_LIST = ("ip_net_list", _("IP prefix/range list"))
    BOOL = ("bool", _("boolean"))  # 'true', '1', 'false' or '0'
    STR = ("str", _("text"))
