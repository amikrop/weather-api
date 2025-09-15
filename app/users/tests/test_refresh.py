import pytest

from users.tests.utils import assert_token_authenticates_user, assert_user_anonymous

pytestmark = pytest.mark.django_db


def test_refresh_success(client, user):
    user.set_password("asd#456")
    user.save()
    assert_user_anonymous()

    response = client.post(
        "/auth/login/", data={"username": "john", "password": "asd#456"}
    )
    data = response.json()
    refresh_token = data["refresh"]
    response = client.post("/auth/refresh/", data={"refresh": refresh_token})
    data = response.json()

    assert response.status_code == 200
    assert set(data) == {"access"}
    assert_token_authenticates_user(data["access"], user)


def test_refresh_missing_required_fields(client):
    response = client.post("/auth/refresh/")
    data = response.json()

    assert response.status_code == 400
    assert "refresh" in data
    assert_user_anonymous()


def test_refresh_wrong_credentials(client):
    response = client.post(
        "/auth/login/", data={"username": "john", "password": "wrong.789"}
    )

    assert response.status_code == 401
    assert_user_anonymous()


def test_refresh_invalid_token(client):
    response = client.post("/auth/refresh/", data={"refresh": "invalid-token"})
    data = response.json()

    assert response.status_code == 401
    assert data["code"] == "token_not_valid"
    assert_user_anonymous()
