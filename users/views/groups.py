from typing import Any

from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from users.forms import GroupForm
from users.models.group import Group


class GroupListView(BaseListView):
    model = Group
    ordering = ("name",)
    template_name = "groups/list.html"
    permission_required = "auth.view_group"


class GroupCreateView(BaseCreateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/create.html"
    permission_required = "auth.add_group"

    def get_form_kwargs(self) -> dict[str, Any]:
        return {**super().get_form_kwargs(), "user": self.request.user}


class GroupDetailView(BaseDetailView):
    model = Group
    template_name = "groups/detail.html"
    permission_required = "auth.view_group"


class GroupUpdateView(BaseUpdateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/update.html"
    permission_required = "auth.change_group"

    def get_form_kwargs(self) -> dict[str, Any]:
        return {**super().get_form_kwargs(), "user": self.request.user}


class GroupDeleteView(BaseDeleteView):
    model = Group
    template_name = "groups/delete.html"
    permission_required = "auth.delete_group"
