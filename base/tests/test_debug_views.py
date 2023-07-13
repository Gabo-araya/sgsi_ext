from base.views.debug import get_sorted_request_variable


def test_get_sorted_request_variable(rf):
    variable_dict = {"b": 1, "a": 2}
    assert get_sorted_request_variable(variable_dict) == {"a": 2, "b": 1}
    request = rf.get("/?b=1&a=2")
    assert get_sorted_request_variable(request.GET) == {"a": "2", "b": "1"}
