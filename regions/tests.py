from http import HTTPStatus
from urllib.parse import urlencode

from django.db.models import CharField
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Cast
from django.db.models.functions import Concat
from django.urls import reverse

from regions.models import Commune


def test_search_communes_by_name(regular_user_client):
    # given
    query_data = {"commune": "Osorno"}

    # when
    url = reverse("search_communes")
    response = regular_user_client.get(url + f"?{urlencode(query_data)}")

    # then
    assert response.status_code == HTTPStatus.OK
    parsed_content = response.json()

    expected_communes = list(
        Commune.objects.annotate(
            text=Concat(Cast("id", CharField()), Value(" - "), F("name"))
        )
        .filter(name="Osorno")
        .values("id", "text")
        .order_by("id")
    )

    assert parsed_content == expected_communes


def test_search_communes_by_id(regular_user_client):
    # given
    query_data = {"regionId": 11}  # see fixtures/initial_data.json

    # when
    url = reverse("search_communes")
    response = regular_user_client.get(url + f"?{urlencode(query_data)}")

    # then
    assert response.status_code == HTTPStatus.OK
    parsed_content = response.json()

    expected_communes = list(
        Commune.objects.annotate(
            text=Concat(Cast("id", CharField()), Value(" - "), F("name"))
        )
        .filter(region_id=11)
        .values("id", "text")
        .order_by("id")
    )

    assert parsed_content == expected_communes
