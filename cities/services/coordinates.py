from __future__ import annotations

import math
from typing import TYPE_CHECKING

import requests
from django.conf import settings
import geocoder
from geopy import distance
from requests import RequestException

from cities.custom_types import GeoResults

if TYPE_CHECKING:
    from cities.models import City


def get_geo_results(location: str) -> GeoResults:
    coordinates_result = get_google_geo_result(location)
    if coordinates_result and coordinates_result.elevation:
        return coordinates_result

    return get_yandex_geo_result(location)


def get_distance(requested_lon: float, requested_lat: float, city: City) -> float | None:
    if city.longitude is None or city.latitude is None:
        return None

    requested_elevation = get_google_elevation_result(requested_lat, requested_lon)
    if not requested_elevation:
        requested_elevation = get_open_elevation_result(requested_lat, requested_lon)
    flat_distance = distance.distance((requested_lat, requested_lon), (city.latitude, city.longitude)).km
    if city.elevation is None or requested_elevation is None:
        return flat_distance

    euclidian_distance = math.sqrt(flat_distance ** 2 + (float(city.elevation) - requested_elevation) ** 2)

    return euclidian_distance


def get_google_geo_result(location: str) -> GeoResults | None:
    geocoder_result = geocoder.google(location)
    if not geocoder_result.ok:
        return None

    lat, lon = geocoder_result.latlng

    elevation = get_google_elevation_result(lat, lon)

    if not elevation:
        elevation = get_open_elevation_result(lat, lon)

    return GeoResults(lat=lat, lon=lon, elevation=elevation)


def get_yandex_geo_result(location: str) -> GeoResults | None:
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {'geocode': location, 'apikey': settings.YANDEX_API_KEY, 'format': 'json'}

    try:
        response = requests.get(base_url, params=params)
    except RequestException:
        return None

    if not response.ok:
        return GeoResults(lat=None, lon=None, elevation=None)

    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')

    elevation = get_open_elevation_result(lat=lat, lon=lon)

    return GeoResults(lat=lat, lon=lon, elevation=elevation)


def get_google_elevation_result(lat, lon) -> float | None:
    geocoder_elevation_result = geocoder.google([lat, lon], method='elevation')

    if not geocoder_elevation_result.ok:
        return None

    return geocoder_elevation_result.meters


def get_open_elevation_result(lat: float, lon: float) -> float | None:
    base_url = 'https://api.open-elevation.com/api/v1/lookup'
    params = {'location': f'{lat},{lon}'}

    try:
        response = requests.get(base_url, params=params)
    except RequestException:
        return None

    if not response.ok:
        return None

    return response.json()['results'][0]['elevation']
