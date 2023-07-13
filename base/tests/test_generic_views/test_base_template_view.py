from contextlib import nullcontext as does_not_raise

from django.core.exceptions import ImproperlyConfigured

import pytest

from base.views.generic import BaseTemplateView


@pytest.mark.parametrize(
    ("title", "expectation"),
    (("Test Title", does_not_raise()), (None, pytest.raises(ImproperlyConfigured))),
)
def test_base_template_view(title, expectation):
    with expectation:
        view = BaseTemplateView()
        view.title = title
        assert view.get_title() == title


def test_base_template_view_context_data():
    view = BaseTemplateView()
    view.title = "Test Title"
    context_data = view.get_context_data()
    assert context_data["title"] == "Test Title"
