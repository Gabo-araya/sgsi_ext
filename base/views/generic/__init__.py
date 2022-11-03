from base.views.generic.base import BaseRedirectView
from base.views.generic.base import BaseTemplateView
from base.views.generic.base import BaseView
from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseSubModelCreateView
from base.views.generic.edit import BaseUpdateRedirectView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView

__all__ = [
    "BaseView",
    "BaseTemplateView",
    "BaseRedirectView",
    "BaseDetailView",
    "BaseCreateView",
    "BaseDeleteView",
    "BaseUpdateView",
    "BaseSubModelCreateView",
    "BaseUpdateRedirectView",
    "BaseListView",
]
