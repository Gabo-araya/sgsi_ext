from django import template

from base.utils import build_absolute_url_wo_req

register = template.Library()


@register.filter
def path_to_uri(path: str) -> str:
    return build_absolute_url_wo_req(path)
