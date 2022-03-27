from typing import Mapping

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_serializer
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cities.models import City
from cities.serializers import CitySerializer
from cities.utils.handle_city_query import get_closest_cities_ids, get_cities_qs


class CitiesListView(ListAPIView):
    queryset = City.objects
    serializer_class = CitySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='latitude',
                description='City latitude',
                required=False,
                type=float,
                examples=[
                    OpenApiExample(
                        name='Latitude example',
                        description='Example of query parameters latitude',
                        value='37.2',
                    ),
                ],
            ),
            OpenApiParameter(
                name='longitude',
                description='City longitude',
                required=False,
                type=float,
                examples=[
                    OpenApiExample(
                        name='Longitude example',
                        description='Example of query parameters longitude',
                        value='54',
                    ),
                ],
            ),
        ],
        examples=[
            OpenApiExample(
                name='Response cities example',
                description='Response cities example',
                value={
                    "title": "Super city",
                    "latitude": "100.3",
                    "longitude": "34.8",
                    "elevation": "12"
                }
            )
        ]
    )
    def get(self, request: Request, **kwargs: Mapping) -> Response:
        cities_closest_ids: list[int] | None = None
        try:
            requested_lat = float(request.query_params['lat']) if request.query_params.get('lat') else None
        except ValueError:
            return Response(
                data={'message': f'Query parameters lat should be int or float instead {request.query_params["lat"]}'},
                status=status.HTTP_200_OK,
            )
        try:
            requested_lon = float(request.query_params['lon']) if request.query_params.get('lon') else None
        except ValueError:
            return Response(
                data={'message': f'Query parameters lon should be int or float instead {request.query_params["lon"]}'},
                status=status.HTTP_200_OK,
            )
        if requested_lat is not None and requested_lon is not None:
            cities_closest_ids = get_closest_cities_ids(requested_lat, requested_lon)

        cities_qs = get_cities_qs(cities_closest_ids)

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

    @extend_schema(
        request=CitySerializer,
        responses={201: CitySerializer},
    )
    def post(self, request: Request, **kwargs: Mapping) -> Response:
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
