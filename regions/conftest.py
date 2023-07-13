import pytest

from regions.models import Commune
from regions.models import Region


@pytest.fixture
def region(db):
    return Region.objects.create(name="region")


@pytest.fixture
def commune(region, db):
    return Commune.objects.create(name="commune", region=region)
