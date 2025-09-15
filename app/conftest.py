from datetime import datetime, timezone

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from weather.models import Station
from weather.settings import DEFAULTS, app_settings

User = get_user_model()


@pytest.fixture(autouse=True)
def use_default_settings(monkeypatch):
    for key, value in DEFAULTS.items():
        monkeypatch.setattr(app_settings, key, value)

    monkeypatch.setitem(
        settings.REST_FRAMEWORK, "PAGE_SIZE", settings.DEFAULT_PAGE_SIZE
    )


@pytest.fixture(autouse=True)
def user():
    return User.objects.create_user(
        "john", "john@example.com", first_name="John", last_name="Doe"
    )


@pytest.fixture
def client_authed(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def station():
    return Station.objects.create(
        name="Paris Station", latitude=48.8566, longitude=2.3522, elevation=35
    )


@pytest.fixture
def other_station():
    return Station.objects.create(
        name="Tokyo Station", latitude=35.6895, longitude=139.6917, elevation=40
    )


@pytest.fixture
def measurement(station):
    return station.measurement_set.create(
        datetime=datetime(2024, 5, 10, 14, 5, 28, tzinfo=timezone.utc),
        temperature=19,
        humidity=45.8,
        wind_speed=2,
        wind_direction="S",
        rainfall=1.6,
    )
