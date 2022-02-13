from cities.models import City
from cities.services.coordinates import get_distance


def get_closest_cities_qs(params) -> list[int] | None:
    cities = City.objects.filter(latitude__isnull=False, longitude__isnull=False)
    requested_lat = float(params['lat']) if params.get('lat') else None
    requested_lon = float(params['lon']) if params.get('lon') else None
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
