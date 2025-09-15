from django.urls import include, path
from rest_framework.routers import DefaultRouter

from weather.views import MeasurementViewSet, StationViewSet

router = DefaultRouter()
router.register("stations", StationViewSet, basename="station")
router.register("measurements", MeasurementViewSet, basename="measurement")

urlpatterns = [path("", include(router.urls))]
