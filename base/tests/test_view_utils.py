import pytest

from base.view_utils import paginate


@pytest.mark.parametrize(
    ("page", "objects", "expected_page", "expected_objects"),
    (
        (None, range(100), 1, range(25)),
        (2, range(100), 2, range(25, 50)),
        (4, range(100), 4, range(75, 100)),
        (25, range(100), 4, range(75, 100)),
    ),
)
def test_paginate(page, objects, expected_page, expected_objects, rf):
    request = rf.get(f"/?p={page}")
    paginated_objects = paginate(request, objects)
    assert paginated_objects.number == expected_page
    assert paginated_objects.object_list == expected_objects
