# django
from django import template
from django.conf import settings
from django.template.loader import get_template

register = template.Library()


def return_empty_context():
    return ""


def env_badge():
    """Displays a tag depending on the environment the app is running on."""
    if settings.DEBUG:
        return {"app_environment": "debug"}
    else:
        return {"app_environment": "staging"}


if not settings.CRITICAL_ENVIRONMENT:
    register.inclusion_tag(get_template("includes/environment_badge.pug"))(env_badge)
else:
    register.simple_tag(return_empty_context, name="env_badge")
