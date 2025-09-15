import pytest

pytestmark = pytest.mark.django_db


def test_station_detail_success(client, station):
    response = client.get(f"/stations/{station.id}/")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "id": station.id,
        "name": "Paris Station",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "elevation": 35,
    }


def test_station_detail_not_found(client):
    response = client.get("/stations/380/")
    assert response.status_code == 404
