import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

User = get_user_model()


def test_register_success(client):
    assert User.objects.count() == 1
    response = client.post(
        "/auth/register/",
        data={
            "email": "bugs.bunny@test.org",
            "username": "bugs",
            "password": "abc12345678",
            "first_name": "Bugs",
            "last_name": "Bunny",
        },
    )
    data = response.json()
    user = User.objects.get(username="bugs")

    assert response.status_code == 201
    assert data == {
        "email": "bugs.bunny@test.org",
        "username": "bugs",
        "first_name": "Bugs",
        "last_name": "Bunny",
    }
    assert user.email == "bugs.bunny@test.org"
    assert user.username == "bugs"
    assert user.first_name == "Bugs"
    assert user.last_name == "Bunny"
    assert user.check_password("abc12345678")
    assert User.objects.count() == 2


def test_register_success_missing_optional_fields(client):
    assert User.objects.count() == 1
    response = client.post(
        "/auth/register/",
        data={
            "email": "mickey.mouse@example.com",
            "username": "mickey",
            "password": "567$zxc12",
        },
    )
    data = response.json()
    user = User.objects.get(username="mickey")

    assert response.status_code == 201
    assert data == {"email": "mickey.mouse@example.com", "username": "mickey"}
    assert user.email == "mickey.mouse@example.com"
    assert user.username == "mickey"
    assert user.check_password("567$zxc12")
    assert User.objects.count() == 2


@pytest.mark.parametrize("missing_field", ["email", "username", "password"])
def test_register_missing_required_fields(client, missing_field):
    assert User.objects.count() == 1
    input_data = {
        "email": "foo@test.com",
        "username": "foo",
        "password": "45678abcdefg",
    }
    del input_data[missing_field]

    response = client.post("/auth/register/", data=input_data)
    data = response.json()

    assert response.status_code == 400
    assert missing_field in data
    assert User.objects.count() == 1


def test_register_invalid_email(client):
    assert User.objects.count() == 1
    response = client.post(
        "/auth/register/",
        data={"email": "abc", "username": "abcde", "password": "888xyz12345"},
    )
    data = response.json()

    assert response.status_code == 400
    assert "email" in data
    assert User.objects.count() == 1


@pytest.mark.parametrize("field", ["username", "first_name", "last_name"])
def test_register_field_too_long(client, field):
    assert User.objects.count() == 1
    input_data = {
        "email": "george@example.org",
        "username": "george",
        "password": "7654hjkl345",
        "first_name": "George",
        "last_name": "Stone",
    }
    input_data[field] = "abc123" * 100
    response = client.post("/auth/register/", data=input_data)
    data = response.json()

    assert response.status_code == 400
    assert field in data
    assert User.objects.count() == 1


def test_register_invalid_password(client):
    assert User.objects.count() == 1
    response = client.post(
        "/auth/register/",
        data={"email": "baz12@example.com", "username": "baz12", "password": "78er"},
    )
    data = response.json()

    assert response.status_code == 400
    assert "password" in data
    assert User.objects.count() == 1


def test_register_existing_email(client):
    assert User.objects.count() == 1
    response = client.post(
        "/auth/register/",
        data={
            "email": "john@example.com",
            "username": "someone1",
            "password": "some-pass-123",
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert "email" in data
    assert User.objects.count() == 1


def test_register_existing_username(client):
    assert User.objects.count() == 1
    response = client.post(
        "/auth/register/",
        data={
            "email": "asdf@testing.com",
            "username": "john",
            "password": "12hjkl6789",
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert "username" in data
    assert User.objects.count() == 1
