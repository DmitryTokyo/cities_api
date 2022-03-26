from django.contrib import admin
from django.urls import path, include
from cities_app.spectacular import urlpatterns as swagger_url

urlpatterns = [
    path('api/v1/', include('cities.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += swagger_url

