from rest_framework.routers import DefaultRouter

from .viewsets import DummyAuthenticatedViewset
from .viewsets import DummyViewset

app_name = "dummy-app"
router = DefaultRouter()

router.register(r"dummy", DummyViewset, basename="dummy")
router.register(r"auth/dummy", DummyAuthenticatedViewset, basename="auth-dummy")

urlpatterns = router.urls
