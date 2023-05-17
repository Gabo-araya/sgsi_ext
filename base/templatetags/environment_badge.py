from django import template
from django.conf import settings
from django.template.loader import get_template

register = template.Library()


def return_empty_context():
    return ""


def env_badge():
    """Displays a tag depending on the environment the app is running on."""
    return {"app_environment": "debug" if settings.DEBUG else settings.ENVIRONMENT_NAME}


if not settings.DEBUG and settings.ENVIRONMENT_NAME == "production":
    register.simple_tag(return_empty_context, name="env_badge")
else:
    register.inclusion_tag(get_template("includes/environment_badge.html"))(env_badge)
