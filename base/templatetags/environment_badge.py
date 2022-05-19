# django
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("includes/environment_badge.pug")
def env_badge():
    """Displays a tag depending on the environment the app is running on."""
    if settings.CRITICAL_ENVIRONMENT:
        return {"app_environment": "production"}
    elif settings.DEBUG:
        return {"app_environment": "debug"}
    else:
        return {"app_environment": "staging"}
