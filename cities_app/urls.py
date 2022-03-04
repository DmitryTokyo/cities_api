from django.contrib import admin
from django.urls import path, include
from cities_app.yasg import urlpatterns as doc_url

urlpatterns = [
    path('api/v1/', include('cities.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += doc_url

