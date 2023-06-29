from http import HTTPStatus
from urllib.parse import urlencode

from django.db.models import CharField
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Cast
from django.db.models.functions import Concat
from django.urls import reverse

from base.tests import BaseTestCase
from regions.models import Commune
from regions.models import Region


class RegionViewsTests(BaseTestCase):
    def test_search_communes_by_name(self):
        # given
        query_data = {"commune": "Osorno"}

        # when
        url = reverse("search_communes")
        response = self.client.get(url + f"?{urlencode(query_data)}")

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        parsed_content = response.json()

        expected_communes = list(
            Commune.objects.annotate(
                text=Concat(Cast("id", CharField()), Value(" - "), F("name"))
            )
            .filter(name="Osorno")
            .values("id", "text")
            .order_by("id")
        )

        self.assertEqual(parsed_content, expected_communes)

    def test_search_communes_by_id(self):
        region_ten = Region.objects.get(order=10)

        # given
        query_data = {"regionId": region_ten.pk}

        # when
        url = reverse("search_communes")
        response = self.client.get(url + f"?{urlencode(query_data)}")

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        parsed_content = response.json()

        expected_communes = list(
            Commune.objects.annotate(
                text=Concat(Cast("id", CharField()), Value(" - "), F("name"))
            )
            .filter(region_id=region_ten.pk)
            .values("id", "text")
            .order_by("id")
        )

        self.assertEqual(parsed_content, expected_communes)
