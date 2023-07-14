from typing import NamedTuple

from django import template
from django.utils.http import urlencode

register = template.Library()


class OrderingParameter(NamedTuple):
    field: str
    reverse: bool = False

    def __invert__(self):
        return OrderingParameter(self.field, not self.reverse)

    def __str__(self):
        return f"-{self.field}" if self.reverse else self.field

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        if not isinstance(other, OrderingParameter):
            msg = f"Cannot compare with {type(other).__name}"
            raise TypeError(msg)
        return self.field == other.field and self.reverse == other.reverse

    @classmethod
    def from_str(cls, value):
        return cls(value.lstrip("-"), value.startswith("-"))


@register.simple_tag
def get_order_by_querystring(ordering, current_order=None, remove=False):
    """
    Using the ordering parameter (a list), returns a query string with the
    orders of the columns

    The parameter current_order can be passed along to handle the specific
    order of a single column. So for example if you are ordering by 'email' and
    'first_name', you can pass on 'email' as the current order, so the system
    can preserve the existing ordering, inverting only the email field.
    """

    params = {"o": ordering}

    if not current_order:
        return urlencode(params, doseq=True)

    ordering = [OrderingParameter.from_str(order) for order in ordering]
    current_order = OrderingParameter.from_str(current_order)
    ordering_params = []

    for order in ordering:
        value = order
        if value.field == current_order.field:
            if remove:
                continue
            value = ~value
        ordering_params.append(value)

    if current_order.field not in (o.field for o in ordering):
        ordering_params.append(current_order)

    params = {"o": ordering_params}

    return urlencode(params, doseq=True)
