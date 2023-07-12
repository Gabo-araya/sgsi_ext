import pytest

from inflection import underscore

from base.fixtures import MODEL_FIXTURE_CUSTOM_NAMES
from base.utils import get_our_models


@pytest.mark.django_db(databases=["default", "logs"])
def test_all_models_have_fixtures(request):
    """Checks all our models have at least a test fixture defined."""
    models_without_fixtures = []

    for model_class in get_our_models():
        fixture_name = get_fixture_name_for_model(model_class)
        fixture = request.getfixturevalue(fixture_name)
        if not fixture:
            models_without_fixtures.append((model_class, fixture_name))
            continue
        assert isinstance(fixture, model_class), (
            f'Fixture "{fixture_name}" did not return'
            f" an {model_class.__name__} instance!"
        )

    assert not models_without_fixtures, (
        "Found model(s) without defined test fixture(s): \n"
        + "\n".join(
            f"* {model_class._meta.app_label}.{model_class.__name__} "
            f'(should be called "{model_name}")'
            for model_class, model_name in models_without_fixtures
        )
        + "\nEnsure fixtures with the above mentioned names exist and are "
        "available globally."
    )


def get_fixture_name_for_model(model_class):
    try:
        model_name = underscore(model_class.__name__)
        django_name = f"{model_class._meta.app_label}.{model_class.__name__}"
        return MODEL_FIXTURE_CUSTOM_NAMES.get(django_name, model_name)
    except pytest.FixtureLookupError:
        return None
