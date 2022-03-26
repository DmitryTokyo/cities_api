from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db

def test_cities_list_views(client):
    url = reverse('cities:cities')
    response = client.get(url)

    assert response.status_code == 200
