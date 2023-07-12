import pytest

from regions.models import Commune
from regions.models import Region


@pytest.fixture
def region(db) -> Region:
    return Region.objects.create(
        name="Región de Prueba", short_name="De Prueba", order=10, importance=1
    )


@pytest.fixture
def commune(region) -> Commune:
    return Commune.objects.create(region=region, name="Testing")
