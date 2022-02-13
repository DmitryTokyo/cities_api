from decimal import Decimal

from django.db import models
from django_lifecycle import LifecycleModelMixin, BEFORE_CREATE, hook

from cities.services.coordinates import get_geo_results


class City(LifecycleModelMixin, models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
        verbose_name_plural = 'Cities'

    title = models.CharField('city', max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    elevation = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    @property
    def coordinates(self) -> tuple[Decimal | None, Decimal | None, Decimal | None]:
        return self.latitude, self.longitude, self.elevation

    @hook(BEFORE_CREATE)
    def create_city_coordinates(self) -> None:
        geo_result = get_geo_results(self.title)
        self.longitude, self.latitude, self.elevation = geo_result.lon, geo_result.lat, geo_result.elevation
