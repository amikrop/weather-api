import pytest

from weather.models import Measurement

pytestmark = pytest.mark.django_db


def test_measurement_update_success(client_authed, station, measurement):
    response = client_authed.put(
        f"/measurements/{measurement.id}/",
        data={
            "temperature": 20,
            "humidity": 45.8,
            "wind_speed": 2.5,
            "wind_direction": "S",
            "rainfall": 1.7,
        },
    )
    data = response.json()
    measurement = Measurement.objects.get(id=measurement.id)

    assert response.status_code == 200
    assert data == {
        "id": measurement.id,
        "datetime": "2024-05-10T14:05:28Z",
        "temperature": 20,
        "humidity": 45.8,
        "wind_speed": 2.5,
        "wind_direction": "S",
        "rainfall": 1.7,
        "station": {"id": station.id, "name": station.name},
    }
    assert measurement.temperature == 20
    assert measurement.humidity == 45.8
    assert measurement.wind_speed == 2.5
    assert measurement.wind_direction == "S"
    assert measurement.rainfall == 1.7
    assert measurement.station == station


def test_measurement_update_not_found(client_authed):
    response = client_authed.put(
        "/measurements/1003/",
        data={
            "temperature": 15,
            "humidity": 70,
            "wind_speed": 2,
            "wind_direction": "S",
            "rainfall": 1.78,
        },
    )

    assert response.status_code == 404


def test_measurement_update_unauthenticated(client):
    response = client.put(
        "/measurements/2000/",
        data={
            "temperature": 18,
            "humidity": 70,
            "wind_speed": 2,
            "wind_direction": "S",
            "rainfall": 1.2,
        },
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "field,value",
    [
        ("temperature", -101.7),
        ("temperature", 95.36),
        ("humidity", -3.0),
        ("humidity", 141.9),
        ("wind_speed", -7.8),
        ("wind_speed", 184.57),
        ("rainfall", -12.6),
        ("rainfall", 712),
    ],
)
def test_measurement_update_invalid_values(
    client_authed, station, measurement, field, value
):
    response = client_authed.put(
        f"/measurements/{measurement.id}/",
        data={
            "datetime": "2023-05-10T14:05:28Z",
            "temperature": 21.4,
            "humidity": 58.2,
            "wind_speed": 4.1,
            "wind_direction": "N",
            "rainfall": 2.7,
            "station_id": station.id,
            field: value,
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert field in data
