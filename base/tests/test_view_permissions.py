from django.contrib.auth.models import Permission
from django.urls import get_resolver


def get_all_views_with_permissions(urlpatterns):
    views = set()
    for pattern in urlpatterns:
        if hasattr(pattern, "url_patterns"):
            views |= get_all_views_with_permissions(pattern.url_patterns)
        else:
            if hasattr(pattern.callback, "cls"):
                view = pattern.callback.cls
            elif hasattr(pattern.callback, "view_class"):
                view = pattern.callback.view_class
            else:
                view = pattern.callback
            if hasattr(view, "permission_required"):
                views.add(view)
    return views


def test_view_permissions(db):
    """Test that all views have a permission defined."""
    urlpatterns = get_resolver(None).url_patterns
    views = get_all_views_with_permissions(urlpatterns)
    for view in views:
        perms = view.permission_required
        perms = [perms] if isinstance(perms, str) else perms
        perms = [perm.split(".") for perm in perms]
        assert all(
            len(perm) == 2 for perm in perms
        ), f"Permission {view.permission_required} is not valid"
        for app_label, codename in perms:
            assert Permission.objects.filter(
                content_type__app_label=app_label, codename=codename
            ).exists(), f"Permission {app_label}.{codename} does not exist"
