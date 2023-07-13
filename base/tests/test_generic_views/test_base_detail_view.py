from base.tests.test_generic_views.mock_model import MockModel
from base.views.generic import BaseDetailView


class MockDetailView(BaseDetailView):
    model = MockModel


def test_base_detail_view():
    view = MockDetailView()
    view.object = MockModel
    context_data = view.get_context_data()
    assert context_data["title"] == "Mock Model: Object"
    assert context_data["opts"] == MockModel._meta
