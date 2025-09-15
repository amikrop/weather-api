import pytest

from weather.models import Station

pytestmark = pytest.mark.django_db


def test_station_delete_success(client_authed, station):
    queryset = Station.objects.filter(id=station.id)
    assert queryset.exists()

    response = client_authed.delete(f"/stations/{station.id}/")
    data = response.content
    queryset = Station.objects.filter(id=station.id)

    assert response.status_code == 204
    assert not data
    assert not queryset.exists()


def test_station_delete_not_found(client_authed):
    response = client_authed.delete("/stations/276/")
    assert response.status_code == 404


def test_station_delete_unauthenticated(client):
    response = client.delete("/stations/47/")
    assert response.status_code == 401
