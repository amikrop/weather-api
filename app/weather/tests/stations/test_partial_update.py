import pytest

from weather.models import Station

pytestmark = pytest.mark.django_db


def test_station_partial_update_success(client_authed, station):
    response = client_authed.patch(
        f"/stations/{station.id}/", data={"name": "Paris Central", "latitude": 48.857}
    )
    data = response.json()
    station = Station.objects.get(id=station.id)

    assert response.status_code == 200
    assert data == {
        "id": station.id,
        "name": "Paris Central",
        "latitude": 48.857,
        "longitude": 2.3522,
        "elevation": 35,
    }
    assert station.id == station.id
    assert station.name == "Paris Central"
    assert station.latitude == 48.857
    assert station.longitude == 2.3522
    assert station.elevation == 35


def test_station_partial_update_not_found(client_authed):
    response = client_authed.patch("/stations/785/", data={"latitude": 48})
    assert response.status_code == 404


def test_station_partial_update_unauthenticated(client):
    response = client.patch("/stations/102/", data={"longitude": 2.3})
    assert response.status_code == 401


@pytest.mark.parametrize(
    "field,value",
    [
        ("latitude", -92.42),
        ("latitude", 117.6),
        ("longitude", -199),
        ("longitude", 207),
        ("elevation", -564.2),
        ("elevation", 9321.7),
    ],
)
def test_station_partial_update_invalid_values(client_authed, station, field, value):
    response = client_authed.patch(f"/stations/{station.id}/", data={field: value})
    data = response.json()

    assert response.status_code == 400
    assert field in data
