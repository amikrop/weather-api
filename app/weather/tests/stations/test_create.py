import pytest

from weather.models import Station

pytestmark = pytest.mark.django_db


def test_station_create_success(client_authed):
    response = client_authed.post(
        "/stations/",
        data={
            "name": "Oslo Station",
            "latitude": 59.9139,
            "longitude": 10.7522,
            "elevation": 23,
        },
    )
    data = response.json()
    station_id = data.pop("id")
    station = Station.objects.get(id=station_id)

    expected_data = {
        "name": "Oslo Station",
        "latitude": 59.9139,
        "longitude": 10.7522,
        "elevation": 23,
    }

    assert response.status_code == 201
    assert data == expected_data
    assert Station.objects.count() == 1

    assert isinstance(station_id, int)
    assert station.name == expected_data["name"]
    assert station.latitude == expected_data["latitude"]
    assert station.longitude == expected_data["longitude"]
    assert station.elevation == expected_data["elevation"]


def test_station_create_unauthenticated(client):
    response = client.post(
        "/stations/",
        data={
            "name": "Madrid Station",
            "latitude": 40.4168,
            "longitude": -3.7038,
            "elevation": 667,
        },
    )

    assert response.status_code == 401
    assert Station.objects.count() == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("latitude", -135),
        ("latitude", 91.53),
        ("longitude", -186),
        ("longitude", 181.551),
        ("elevation", -620.2),
        ("elevation", 9100),
    ],
)
def test_station_create_invalid_values(client_authed, field, value):
    response = client_authed.post(
        "/stations/", data={"name": "Test Station", field: value}
    )
    data = response.json()

    assert response.status_code == 400
    assert field in data
    assert Station.objects.count() == 0
