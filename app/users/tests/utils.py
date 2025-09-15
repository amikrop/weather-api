from rest_framework.test import APIRequestFactory

from weather.views import MeasurementViewSet

factory = APIRequestFactory()
view = MeasurementViewSet.as_view({"get": "list"})


def assert_user_anonymous():
    request = factory.get("/measurements/")
    view(request)
    assert request.user.is_anonymous


def assert_token_authenticates_user(access_token, user):
    request = factory.get("/measurements/", HTTP_AUTHORIZATION=f"Bearer {access_token}")
    view(request)
    assert request.user == user
    assert request.user.is_authenticated
