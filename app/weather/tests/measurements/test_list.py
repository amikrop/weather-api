import pytest

pytestmark = pytest.mark.django_db


def test_measurement_list_success(client, station, other_station, measurement):
    other_measurement = other_station.measurement_set.create(
        datetime="2024-05-10T14:06:30Z",
        temperature=21,
        humidity=42,
        wind_speed=3.4,
        wind_direction="SW",
        rainfall=2.1,
    )
    response = client.get("/measurements/")
    data = response.json()["results"]

    assert response.status_code == 200
    assert len(data) == 2
    assert data == [
        {
            "id": other_measurement.id,
            "datetime": "2024-05-10T14:06:30Z",
            "temperature": 21,
            "humidity": 42,
            "wind_speed": 3.4,
            "wind_direction": "SW",
            "rainfall": 2.1,
            "station": {"id": other_station.id, "name": other_station.name},
        },
        {
            "id": measurement.id,
            "datetime": "2024-05-10T14:05:28Z",
            "temperature": 19,
            "humidity": 45.8,
            "wind_speed": 2,
            "wind_direction": "S",
            "rainfall": 1.6,
            "station": {"id": station.id, "name": station.name},
        },
    ]
