import pytest

pytestmark = pytest.mark.django_db


def test_station_list_success(client, station, other_station):
    response = client.get("/stations/")
    data = response.json()["results"]

    assert response.status_code == 200
    assert len(data) == 2
    assert data == [
        {
            "id": station.id,
            "name": "Paris Station",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "elevation": 35,
        },
        {
            "id": other_station.id,
            "name": "Tokyo Station",
            "latitude": 35.6895,
            "longitude": 139.6917,
            "elevation": 40,
        },
    ]
