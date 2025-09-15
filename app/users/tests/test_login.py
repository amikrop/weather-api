import pytest

from users.tests.utils import assert_token_authenticates_user, assert_user_anonymous

pytestmark = pytest.mark.django_db


def test_login_success(client, user):
    user.set_password("some.pass778")
    user.save()
    assert_user_anonymous()

    response = client.post(
        "/auth/login/", data={"username": "john", "password": "some.pass778"}
    )
    data = response.json()

    assert response.status_code == 200
    assert set(data) == {"access", "refresh"}
    assert_token_authenticates_user(data["access"], user)


@pytest.mark.parametrize("missing_field", ["username", "password"])
def test_login_missing_required_fields(client, missing_field):
    input_data = {"username": "the_username", "password": "the_password"}
    del input_data[missing_field]

    response = client.post("/auth/login/", data=input_data)
    data = response.json()

    assert response.status_code == 400
    assert missing_field in data
    assert_user_anonymous()


def test_login_wrong_credentials(client):
    response = client.post(
        "/auth/login/", data={"username": "somebody", "password": "wrong-321"}
    )

    assert response.status_code == 401
    assert_user_anonymous()
