import pytest

from weather.models import Measurement

pytestmark = pytest.mark.django_db


@pytest.fixture
def measurements(station, other_station):
    return Measurement.objects.bulk_create(
        [
            Measurement(
                datetime="2020-05-11T09:00:00Z",
                temperature=22,
                humidity=50,
                wind_speed=3,
                wind_direction="NE",
                rainfall=2,
                station=station,
            ),
            Measurement(
                datetime="2022-05-12T16:30:00Z",
                temperature=18,
                humidity=55,
                wind_speed=4,
                wind_direction="W",
                rainfall=0.5,
                station=other_station,
            ),
            Measurement(
                datetime="2024-06-01T12:00:00Z",
                temperature=25,
                humidity=60,
                wind_speed=5,
                wind_direction="N",
                rainfall=3.1,
                station=other_station,
            ),
        ]
    )


@pytest.mark.parametrize(
    "query_template,expected_indices",
    [
        ("station_id={station_id}", {0, 1}),
        ("station_id={other_station_id}", {2, 3}),
        ("station_id={station_id}&station_id={other_station_id}", {0, 1, 2, 3}),
        ("datetime_from=2021-01-12T00:00:00Z", {0, 2, 3}),
        ("datetime_to=2022-09-20", {1, 2}),
        ("datetime_from=2023-12-01&datetime_to=2025-08-02T23:40:02Z", {0, 3}),
        ("station_id={station_id}&datetime_from=2021-01-01", {0}),
    ],
)
def test_search_measurements(
    client,
    measurement,
    measurements,
    station,
    other_station,
    query_template,
    expected_indices,
):
    query_string = query_template.format(
        station_id=station.id, other_station_id=other_station.id
    )

    existing_measurements = [measurement, *measurements]
    measurement_indices = {m.id: index for index, m in enumerate(existing_measurements)}

    response = client.get(f"/measurements/?{query_string}")
    data = response.json()["results"]
    returned_indices = {measurement_indices[m["id"]] for m in data}

    assert response.status_code == 200

    for m in data:
        assert set(m) == {
            "id",
            "datetime",
            "temperature",
            "humidity",
            "wind_speed",
            "wind_direction",
            "rainfall",
            "station",
        }

    assert len(data) == len(expected_indices)
    assert returned_indices == expected_indices
