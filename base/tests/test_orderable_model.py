from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from base.models import OrderableModel


class OrderbaleModelMagicMock(MagicMock):
    def __init__(self):
        super().__init__()
        self.__class__ = MagicMock()
        self.__class__.objects.count.return_value = 5


@pytest.mark.parametrize(
    ("pk", "expected_calls"),
    (
        (None, 1),
        (1, 0),
    ),
)
def test_orderable_model_save(pk, expected_calls):
    with (patch("base.models.base_model.BaseModel.save")):
        instance_mock = MagicMock(spec=OrderableModel)
        instance_mock.pk = pk
        OrderableModel.save(instance_mock)
        assert instance_mock._set_display_order.call_count == expected_calls


def test_set_display_order():
    instance_mock = OrderbaleModelMagicMock()
    OrderableModel._set_display_order(instance_mock)
    assert instance_mock.display_order == 6


def test_reorder_display_order():
    OrderableModel.objects = MagicMock()
    OrderableModel.objects.all.return_value = [MagicMock() for _ in range(5)]
    OrderableModel.reorder_display_order()
    for i in range(5):
        assert OrderableModel.objects.all()[i].display_order == i
