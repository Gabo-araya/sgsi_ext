from __future__ import annotations

import os

from typing import TYPE_CHECKING

from django import template

if TYPE_CHECKING:
    from django.db.models import FieldFile

register = template.Library()


@register.filter
def filename(file: FieldFile) -> str:
    return os.path.basename(file.name)
