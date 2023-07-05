from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase

from translation_manager.models import Chapter, Translation


class TranslationManagerTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = None
        self.http_origin = None
        self.query_params = None
        self.response = None
        self.response_json = None
        self.translation01 = Translation.objects.create(title="Test Translation 01")
        self.translation02 = Translation.objects.create(title="Test Translation 02")
        self.chapter01 = Chapter.objects.create(
            title="Test Chapter 01-01", serial=0, parent_translation=self.translation01
        )
        self.chapter02 = Chapter.objects.create(
            title="Test Chapter 02-01", serial=0, parent_translation=self.translation02
        )

    def set_url(self, url):
        self.url = url

    def set_query_params(self, query_params):
        self.query_params = query_params

    def assertReseponseOk(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def build_request(self):
        r = {}
        if self.query_params is not None:
            r["QUERY_STRING"] = urlencode(self.query_params, doseq=True)
        if self.http_origin is not None:
            r["HTTP_ORIGIN"] = self.http_origin
        return r

    def call_get_method(self):
        self.response = self.client.get(
            self.url, self.query_params, format="json", **self.build_request()
        )
        self.response_json = self.response.json()
        return self.response_json

    def test_translation_list_endpoint_returns_200(self):
        self.set_url(reverse("v1:translations-list"))
        self.call_get_method()
        self.assertReseponseOk()
        self.assertEqual(len(self.response_json["all_translations"]), 2)

    def test_translations_list_search(self):
        self.set_url(reverse("v1:translations-list"))
        self.set_query_params({"q": "02"})
        self.call_get_method()
        self.assertReseponseOk()
        self.assertEqual(len(self.response_json["all_translations"]), 1)
        self.assertIn("02", self.response_json["all_translations"][0]["title"])
