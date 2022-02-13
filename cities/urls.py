from django.urls import path

from cities.views import CityView, CitiesListView

app_name = 'cities'

urlpatterns = [
    path('cities', CitiesListView.as_view(), name='cities'),
    path('cities/<int:pk>', CityView.as_view(), name='city'),
]
