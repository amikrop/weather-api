from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def parse_datetime_safe(datetime_string):
    try:
        datetime_obj = parse_datetime(datetime_string)
    except (TypeError, ValueError):
        return None

    if datetime_obj is not None and timezone.is_naive(datetime_obj):
        return timezone.make_aware(datetime_obj)
    return datetime_obj


def filter_measurements(queryset, request):
    """Return given measurement queryset, filtered by query parameters.

    The station_id query parameter can take a single or multiple values (by passing the
    key value pair multiple times in the URL). Those values connect to each other by
    logical OR operators.

    Parameters datetime_from and datetime_to are single valued, and keep only results
    whose datetime is "greater than or equal to", and "less than or equal to" the given
    value, respectively.

    Ultimately, those filter groups are joined with logical AND operators, and used to
    fetch the end results.
    """
    station_filters = Q()
    station_ids = request.GET.getlist("station_id")
    for station_id in station_ids:
        if station_id.isdigit():
            station_filters |= Q(station_id=station_id)

    datetime_from_filter = Q()
    datetime_from = request.GET.get("datetime_from")
    datetime_obj = parse_datetime_safe(datetime_from)
    if datetime_obj is not None:
        datetime_from_filter = Q(datetime__gte=datetime_obj)

    datetime_to_filter = Q()
    datetime_to = request.GET.get("datetime_to")
    datetime_obj = parse_datetime_safe(datetime_to)
    if datetime_obj is not None:
        datetime_to_filter = Q(datetime__lte=datetime_obj)

    filters = station_filters & datetime_from_filter & datetime_to_filter
    return queryset.filter(filters)
