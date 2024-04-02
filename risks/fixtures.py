import pytest

from risks.enums import LikelihoodChoices
from risks.enums import SeverityChoices
from risks.enums import TreatmentChoices
from risks.models.risk import Risk


@pytest.fixture
@pytest.mark.django_db
def risk(regular_user, asset, control):
    risk = Risk.objects.create(
        title="test risk",
        description="test description",
        responsible=regular_user,
        severity=SeverityChoices.MEDIUM,
        likelihood=LikelihoodChoices.MEDIUM,
        treatment=TreatmentChoices.ACCEPT,
    )
    risk.assets.set([asset])
    risk.controls.set([control])
    return risk
