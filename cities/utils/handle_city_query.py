from django.db.models import QuerySet

from cities.models import City
from cities.services.coordinates import get_distance


def get_closest_cities_ids(requested_lat: float, requested_lon: float) -> list[int] | None:
    cities = City.objects.filter(latitude__isnull=False, longitude__isnull=False)
    if requested_lat is None or requested_lon is None:
        return None
    distance_to_cities = []
    for city in cities:
        distance = get_distance(requested_lon=requested_lon, requested_lat=requested_lat, city=city)
        distance_to_cities.append(
            {
                'id': city.pk,
                'distance': distance,
            },
        )
    sorted_cities_ids = list(map(lambda d: d['id'], sorted(distance_to_cities, key=lambda d: d['distance'])))
    return sorted_cities_ids[:2]


def get_cities_qs(cities_closest_ids: list[int] | None = None) -> QuerySet:
    return City.objects.filter(id__in=cities_closest_ids) if cities_closest_ids else City.objects.all()
