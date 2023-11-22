from django.templatetags.static import static

import project


def build_info(request):
    """
    Context processor that provides Git commit and build time into the context.
    """

    return {
        "build_info": {
            "git_ref": project._GIT_REF,
            "build_time": project._BUILD_TIME,
        }
    }


def react_context(request):
    """Adds the context required by react components."""

    context = {"react_context": {"static_path": static("")}}

    if not request or not hasattr(request, "user"):
        context["react_context"]["user"] = None
        return context

    user = request.user
    if user.is_anonymous:
        context["react_context"]["user"] = None
        return context

    context["react_context"]["user"] = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    return context
