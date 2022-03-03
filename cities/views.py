from typing import Mapping

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cities.models import City
from cities.serializers import CitySerializer
from cities.utils.handle_city_query import get_closest_cities_qs


class CitiesListView(ListAPIView):
    queryset = City.objects

    def get(self, request: Request, **kwargs: Mapping) -> Response:
        cities_ids = get_closest_cities_qs(request.query_params)

        cities_qs = City.objects.filter(id__in=cities_ids) if cities_ids else City.objects.all()

        serializer = CitySerializer(cities_qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CityView(APIView):

    def delete(self, request: Request, pk: int, **kwargs: Mapping):
        city = City.objects.filter(pk=pk).first()
        if not city:
            return Response(data={'message': 'Wrong city id'}, status=status.HTTP_400_BAD_REQUEST)

        city.delete()
        return Response(data={'message': f'City {pk} was delete'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request: Request, pk: int, **kwargs: Mapping):
        city = City.objects.filter(pk=pk).first()
        if not city:
            return Response(data={'message': 'Wrong city id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CitySerializer(city)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, **kwargs: Mapping) -> Response:
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
