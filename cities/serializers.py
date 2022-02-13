from typing import Mapping

from rest_framework import serializers

from cities.models import City


class CitySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    latitude = serializers.DecimalField(max_digits=10, decimal_places=5, required=False)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=5, required=False)
    elevation = serializers.DecimalField(max_digits=6, decimal_places=3, required=False)

    def create(self, validated_data: Mapping) -> City:
        return City.objects.create(**validated_data)
