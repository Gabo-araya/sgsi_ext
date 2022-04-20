from django import template
from django.utils.http import urlencode

register = template.Library()


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

    params = {
        "o": ordering
    }

    if not current_order:
        return urlencode(params, doseq=True)

    reversed_current_order = "-{}".format(current_order)

    ordering_params = []

    for order in ordering:
        if order == current_order:
            if remove:
                continue
            ordering_params.append(reversed_current_order)
        elif order == reversed_current_order:
            if remove:
                continue
            ordering_params.append(current_order)
        else:
            ordering_params.append(order)

    # remove ordering parameters if not declared either as "current_order" or
    # "reversed_current_order"
    if not (current_order in ordering or reversed_current_order in ordering):
        if not remove:
            ordering_params.append(current_order)

    return urlencode(params, doseq=True)
