from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from weather.models import Measurement, Station
from weather.search import filter_measurements
from weather.serializers import MeasurementSerializer, StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="station_id",
                description="Filter by station ID (can pass multiple times).",
                type=OpenApiTypes.INT,
                many=True,
            ),
            OpenApiParameter(
                name="datetime_from",
                description="Return measurements with datetime >= this value.",
                type=OpenApiTypes.DATETIME,
            ),
            OpenApiParameter(
                name="datetime_to",
                description="Return measurements with datetime <= this value.",
                type=OpenApiTypes.DATETIME,
            ),
        ]
    )
)
class MeasurementViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Measurement.objects.select_related("station")

        if self.action == "list":
            return filter_measurements(queryset, self.request)

        return queryset
