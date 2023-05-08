from rest_framework.routers import DefaultRouter

from .viewsets import DummyViewset

router = DefaultRouter()

router.register(r"dummy", DummyViewset, basename="dummy")

urlpatterns = router.urls
