from django.urls import reverse

from helpers.test import TranslationSiteBaseTestCase
from translation_manager.models import Chapter
from user_manager.models import User


class TranslationManagerTestCase(TranslationSiteBaseTestCase):
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
        self.set_user(self.staff_user)
        self.set_url(reverse("v1:chapters-list"))
        self.call_post_method(data=data)
        self.assertResponseCreated()
        self.assertEqual(self.response_json["title"], "Test Chapter 02")
        self.assertEqual(self.response_json["serial"], 1)
        self.assertEqual(
            self.response_json["parent_translation"], self.translation01.id
        )

    def test_patch_chapters(self):
        data = {"contents": "test content."}
        self.set_user(self.superuser)
        self.set_url(reverse("v1:chapters-details", kwargs={"pk": self.chapter01.id}))
        self.call_patch_method(data=data)
        self.assertReseponseOk()
        self.assertEqual(self.response_json["id"], self.chapter01.id)
        self.assertEqual(self.response_json["contents"], "test content.")

    def test_patch_chapters_fail_for_normal_user(self):
        data = {"contents": "test content."}
        self.set_user(self.normal_user)
        self.set_url(reverse("v1:chapters-details", kwargs={"pk": self.chapter01.id}))
        self.call_patch_method(data=data)
        self.assertResponseForbidden()

    def test_post_chapter_fail_for_non_staff_users(self):
        data = {
            "title": "test chapter title",
            "serial": 3,
            "contents": "test content",
            "parent_translation": self.translation01.id,
        }
        self.set_user(self.normal_user)
        self.set_url(reverse("v1:chapters-list"))
        self.call_post_method(data=data)
        self.assertResponseForbidden()

    def test_post_chapter_success_for_staff_users(self):
        data = {
            "title": "test chapter title",
            "serial": 3,
            "contents": "test content",
            "status": "PB",
            "parent_translation": self.translation01.id,
        }
        self.set_user(self.staff_user)
        self.set_url(reverse("v1:chapters-list"))
        self.call_post_method(data=data)
        self.assertResponseCreated()
        self.assertEqual(self.response_json["title"], "test chapter title")
        self.assertEqual(self.response_json["serial"], 3)
        self.assertEqual(self.response_json["contents"], "test content")
