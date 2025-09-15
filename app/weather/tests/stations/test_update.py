import pytest

from weather.models import Station

pytestmark = pytest.mark.django_db


def test_station_update_success(client_authed, station):
    response = client_authed.put(
        f"/stations/{station.id}/",
        data={
            "name": "Paris Main",
            "latitude": 48.857,
            "longitude": 2.36,
            "elevation": 36,
        },
    )
    data = response.json()
    station = Station.objects.get(id=station.id)

    assert response.status_code == 200
    assert data == {
        "id": station.id,
        "name": "Paris Main",
        "latitude": 48.857,
        "longitude": 2.36,
        "elevation": 36,
    }
    assert station.id == station.id
    assert station.name == "Paris Main"
    assert station.latitude == 48.857
    assert station.longitude == 2.36
    assert station.elevation == 36


def test_station_update_not_found(client_authed):
    response = client_authed.put(
        "/stations/789/",
        data={"name": "Unknown", "latitude": 10, "longitude": 20, "elevation": 50},
    )

    assert response.status_code == 404


def test_station_update_unauthenticated(client):
    response = client.put(
        "/stations/300/",
        data={
            "name": "Unauthorized Update",
            "latitude": 30,
            "longitude": 55,
            "elevation": 12,
        },
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "field,value",
    [
        ("latitude", -95.7),
        ("latitude", 128),
        ("longitude", -184.2),
        ("longitude", 263.9),
        ("elevation", -743),
        ("elevation", 9876),
    ],
)
def test_station_update_invalid_values(client_authed, station, field, value):
    response = client_authed.put(
        f"/stations/{station.id}/", data={"name": "Updated Station", field: value}
    )
    data = response.json()

    assert response.status_code == 400
    assert field in data
