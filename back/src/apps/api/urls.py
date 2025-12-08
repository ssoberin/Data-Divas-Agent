from rest_framework.routers import SimpleRouter

from .viewsets import WorkerViewSet


app_name = "api"

router = SimpleRouter()

router.register("worker", WorkerViewSet, basename="worker")

urlpatterns = router.urls