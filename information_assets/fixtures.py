import pytest

from information_assets.enums import ClassificationChoices
from information_assets.enums import CriticalityChoices
from information_assets.models.asset import Asset
from information_assets.models.asset_role import AssetRole
from information_assets.models.asset_type import AssetType


@pytest.fixture
@pytest.mark.django_db
def asset_type():
    return AssetType.objects.create(
        name="test asset type", description="test description"
    )


@pytest.fixture
@pytest.mark.django_db
def asset(regular_user, asset_type):
    return Asset.objects.create(
        owner=regular_user,
        name="test asset",
        description="test description",
        asset_type=asset_type,
        criticality=CriticalityChoices.MEDIUM,
        classification=ClassificationChoices.INTERNAL,
    )


@pytest.fixture
@pytest.mark.django_db
def asset_role(asset):
    return AssetRole.objects.create(asset=asset, name="test asset role")
