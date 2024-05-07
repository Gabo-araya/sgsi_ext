from django.contrib.auth.models import Group
from django.urls import reverse

from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from users.forms import GroupForm


class GroupUrlMixin:
    def get_object_detail_url(self):
        return reverse("group_detail", args=(self.object.pk,))

    def get_success_url(self):
        return self.get_object_detail_url()


class GroupListView(BaseListView):
    model = Group
    ordering = ("name",)
    template_name = "groups/list.html"
    permission_required = "auth.view_group"


class GroupCreateView(GroupUrlMixin, BaseCreateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/create.html"
    permission_required = "auth.add_group"


class GroupDetailView(BaseDetailView):
    model = Group
    template_name = "groups/detail.html"
    permission_required = "auth.view_group"


class GroupUpdateView(GroupUrlMixin, BaseUpdateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/update.html"
    permission_required = "auth.change_group"

    def get_cancel_url(self):
        return self.get_object_detail_url()


class GroupDeleteView(BaseDeleteView):
    model = Group
    template_name = "groups/delete.html"
    permission_required = "auth.delete_group"
