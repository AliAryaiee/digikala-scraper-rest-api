from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Product
from . import utils


class TestProduct(APITestCase):
    """
        docstring
    """

    def test_url_validation(self):
        """
            Check URL Validation
        """
        valid_url = "https://www.digikala.com/product/dkp-7962769/"
        invalid_url = "https://www.digikala.com/product/dk-7962769/"

        response_ok = self.client.post(
            reverse("products-list"),
            {"url": valid_url}
        )
        self.assertEqual(response_ok.status_code, status.HTTP_201_CREATED)

        response_failed = self.client.post(
            reverse("products-list"),
            {"url": invalid_url}
        )
        self.assertEqual(
            response_failed.status_code,
            status.HTTP_404_NOT_FOUND
        )
