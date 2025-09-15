import pytest

from weather.models import Measurement

pytestmark = pytest.mark.django_db


def test_measurement_partial_update_success(client_authed, station, measurement):
    response = client_authed.patch(
        f"/measurements/{measurement.id}/",
        data={"temperature": 22, "wind_speed": 3.3, "rainfall": 2.4},
    )
    data = response.json()
    measurement = Measurement.objects.get(id=measurement.id)

    assert response.status_code == 200
    assert data == {
        "id": measurement.id,
        "datetime": "2024-05-10T14:05:28Z",
        "temperature": 22,
        "humidity": 45.8,
        "wind_speed": 3.3,
        "wind_direction": "S",
        "rainfall": 2.4,
        "station": {"id": station.id, "name": station.name},
    }
    assert measurement.temperature == 22
    assert measurement.humidity == 45.8
    assert measurement.wind_speed == 3.3
    assert measurement.wind_direction == "S"
    assert measurement.rainfall == 2.4
    assert measurement.station == station


def test_measurement_partial_update_not_found(client_authed):
    response = client_authed.patch(
        "/measurements/1100/", data={"temperature": 19, "humidity": 65}
    )

    assert response.status_code == 404


def test_measurement_partial_update_unauthenticated(client, measurement):
    response = client.patch(
        f"/measurements/{measurement.id}/", data={"temperature": 17, "humidity": 55.2}
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "field,value",
    [
        ("temperature", -95.4),
        ("temperature", 87),
        ("humidity", -6.7),
        ("humidity", 132.55),
        ("wind_speed", -4),
        ("wind_speed", 176),
        ("rainfall", -15.9),
        ("rainfall", 689.32),
    ],
)
def test_measurement_partial_update_invalid_values(
    client_authed, station, measurement, field, value
):
    response = client_authed.patch(
        f"/measurements/{measurement.id}/",
        data={"station_id": station.id, field: value},
    )
    data = response.json()

    assert response.status_code == 400
    assert field in data
