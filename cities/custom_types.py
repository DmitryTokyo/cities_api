from typing import NamedTuple


class GeoResults(NamedTuple):
    lat: float | None
    lon: float | None
    elevation: float | None
