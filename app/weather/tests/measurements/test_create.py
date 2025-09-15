import pytest
from django.utils.dateparse import parse_datetime

from weather.models import Measurement

pytestmark = pytest.mark.django_db


def test_measurement_create_success(client_authed, station):
    response = client_authed.post(
        "/measurements/",
        data={
            "datetime": "2023-03-10T12:00:00Z",
            "temperature": 15.5,
            "humidity": 60,
            "wind_speed": 5.2,
            "wind_direction": "NE",
            "rainfall": 2.3,
            "station_id": station.id,
        },
    )
    data = response.json()
    measurement_id = data.pop("id")
    measurement = Measurement.objects.get(id=measurement_id)

    expected_data = {
        "datetime": "2023-03-10T12:00:00Z",
        "temperature": 15.5,
        "humidity": 60,
        "wind_speed": 5.2,
        "wind_direction": "NE",
        "rainfall": 2.3,
        "station": {"id": station.id, "name": station.name},
    }

    assert response.status_code == 201
    assert data == expected_data
    assert Measurement.objects.count() == 1

    assert isinstance(measurement_id, int)
    assert measurement.datetime == parse_datetime(expected_data["datetime"])
    assert measurement.temperature == expected_data["temperature"]
    assert measurement.humidity == expected_data["humidity"]
    assert measurement.wind_speed == expected_data["wind_speed"]
    assert measurement.wind_direction == expected_data["wind_direction"]
    assert measurement.rainfall == expected_data["rainfall"]
    assert measurement.station == station


def test_measurement_create_unauthenticated(client, station):
    response = client.post(
        "/measurements/",
        data={
            "datetime": "2023-04-01T09:00:00Z",
            "temperature": 18,
            "humidity": 70,
            "station_id": station.id,
        },
    )

    assert response.status_code == 401
    assert Measurement.objects.count() == 0


def test_measurement_create_missing_station(client_authed):
    response = client_authed.post(
        "/measurements/",
        data={"datetime": "2023-04-01T09:00:00Z", "temperature": 18, "humidity": 70},
    )
    data = response.json()

    assert response.status_code == 400
    assert "station_id" in data
    assert Measurement.objects.count() == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("temperature", -102),
        ("temperature", 100.52),
        ("humidity", -1),
        ("humidity", 124.8),
        ("wind_speed", -5),
        ("wind_speed", 208.982),
        ("rainfall", -10),
        ("rainfall", 630.44),
    ],
)
def test_measurement_create_invalid_values(client_authed, station, field, value):
    response = client_authed.post(
        "/measurements/",
        data={
            "datetime": "2023-06-01T12:00:00Z",
            field: value,
            "station_id": station.id,
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert field in data
    assert Measurement.objects.count() == 0


def test_measurement_create_duplicate_datetime_station(client_authed, measurement):
    response = client_authed.post(
        "/measurements/",
        data={
            "datetime": measurement.datetime.isoformat(),
            "temperature": 22.6,
            "humidity": 50,
            "station_id": measurement.station.id,
        },
    )

    assert response.status_code == 400
    assert Measurement.objects.count() == 1
