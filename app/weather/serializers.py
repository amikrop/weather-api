from rest_framework import serializers

from weather.models import Measurement, Station
from weather.settings import app_settings


class StationSerializer(serializers.ModelSerializer):
    elevation = serializers.FloatField(
        required=False,
        min_value=app_settings.ELEVATION_MIN,
        max_value=app_settings.ELEVATION_MAX,
    )

    class Meta:
        model = Station
        fields = "__all__"


class StationInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "name"]


class MeasurementSerializer(serializers.ModelSerializer):
    temperature = serializers.FloatField(
        required=False,
        min_value=app_settings.TEMPERATURE_MIN,
        max_value=app_settings.TEMPERATURE_MAX,
    )
    wind_speed = serializers.FloatField(
        required=False, min_value=0, max_value=app_settings.WIND_SPEED_MAX
    )
    rainfall = serializers.FloatField(
        required=False, min_value=0, max_value=app_settings.RAINFALL_MAX
    )

    # Use station_id for writes, and nested station representation for reads
    station_id = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(), source="station", write_only=True
    )
    station = StationInlineSerializer(read_only=True)

    class Meta:
        model = Measurement
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Do not allow updating station or datetime after creation
        if self.instance is not None:
            self.fields["datetime"].read_only = True
            self.fields["station_id"].read_only = True
