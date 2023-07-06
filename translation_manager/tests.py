from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase

from translation_manager.models import Chapter, Translation


class TranslationManagerTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = None
        self.format = None
        self.content_type = None
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

    def assertResponseCreated(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

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

    def call_post_method(self, data):
        self.response = self.client.post(
            self.url,
            data,
            format=self.format or "json",
            content_type=self.content_type,
            **self.build_request()
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

    def test_translation_list_sort(self):
        self.set_url(reverse("v1:translations-list"))
        self.set_query_params({"asc": "false"})
        self.call_get_method()
        self.assertReseponseOk()
        self.assertEqual(len(self.response_json["all_translations"]), 2)
        self.assertGreater(
            self.response_json["all_translations"][0]["title"],
            self.response_json["all_translations"][1]["title"],
        )

    def test_post_translations(self):
        data = {
            "title": "Test Translation 03",
        }
        self.set_url(reverse("v1:translations-list"))
        self.call_post_method(data=data)
        self.assertResponseCreated()
        self.assertEqual(self.response_json["title"], "Test Translation 03")

    def test_translations_details(self):
        self.set_url(
            reverse("v1:translations-details", kwargs={"pk": self.translation01.id})
        )
        self.call_get_method()
        self.assertReseponseOk()
        self.assertEqual(self.response_json["id"], self.translation01.id)
        chapter_no = Chapter.objects.filter(
            parent_translation=self.translation01
        ).count()
        self.assertEqual(len(self.response_json["chapters"]), chapter_no)

    def test_chapter_list_endpoint_returns_200(self):
        self.set_url(reverse("v1:chapters-list"))
        self.call_get_method()
        self.assertReseponseOk()
        self.assertEqual(len(self.response_json["all_chapters"]), 2)

    def test_chapter_details(self):
        self.set_url(reverse("v1:chapters-details", kwargs={"pk": self.chapter01.id}))
        self.call_get_method()
        self.assertReseponseOk()
        self.assertEqual(self.response_json["id"], self.chapter01.id)

    def test_post_chapters(self):
        data = {
            "title": "Test Chapter 02",
            "serial": 1,
            "parent_translation": self.translation01.id,
        }
        self.set_url(reverse("v1:chapters-list"))
        self.call_post_method(data=data)
        self.assertResponseCreated()
        self.assertEqual(self.response_json["title"], "Test Chapter 02")
        self.assertEqual(self.response_json["serial"], 1)
        self.assertEqual(
            self.response_json["parent_translation"], self.translation01.id
        )
