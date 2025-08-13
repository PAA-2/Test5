import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_endpoint(client):
    url = reverse("health")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
