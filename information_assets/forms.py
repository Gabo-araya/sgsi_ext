from typing import Any

from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import BaseModelForm
from information_assets.models.asset import Asset
from information_assets.models.asset_role import AssetRole
from information_assets.models.asset_type import AssetType
from users.models.group import Group
from users.models.user import User


class AssetForm(BaseModelForm):
    class Meta:
        model = Asset
        fields = (
            "name",
            "code",
            "owner",
            "description",
            "asset_types",
            "criticality",
            "classification",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["owner"].label_from_instance = lambda user: user.get_label()


class AssetTypeForm(BaseModelForm):
    class Meta:
        model = AssetType
        fields = (
            "name",
            "description",
        )


class AssetRoleForm(BaseModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        help_text=_("Initial groups of users that will be assigned to this role."),
    )

    class Meta:
        model = AssetRole
        fields = (
            "asset",
            "name",
            "groups",
        )

    def save(self, commit: bool = ...) -> Any:
        instance = super().save(commit)
        if commit:
            groups = self.cleaned_data["groups"]
            instance.users.set(User.objects.filter(groups__in=groups))
        return instance


class AssetRoleChangeForm(BaseModelForm):
    class Meta:
        model = AssetRole
        fields = (
            "name",
            "users",
        )
