from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from translation_manager.models import Chapter, Translation
from user_manager.models import User


class TranslationSiteBaseTestCase(APITestCase):
    def setUp(self):
        self.current_user = None
        self.url = None
        self.format = None
        self.content_type = None
        self.http_origin = None
        self.query_params = None
        self.response = None
        self.response_json = None

        self.normal_user = User.objects.create_user(email="testuser01@gmail.com")
        self.normal_user.set_password("test_password")
        self.normal_user.save()
        self.staff_user = User.objects.create_user(email="teststaffuser01@gmail.com")
        self.staff_user.is_staff = True
        self.staff_user.set_password("test_password")
        self.staff_user.save()
        self.superuser = User.objects.create_superuser(
            email="testsuperuser01@gmail.com", password="testpw"
        )
        self.superuser.save()

        self.translation01 = Translation.objects.create(title="Test Translation 01")
        self.translation02 = Translation.objects.create(title="Test Translation 02")
        self.chapter01 = Chapter.objects.create(
            title="Test Chapter 01-01", serial=0, parent_translation=self.translation01
        )
        self.chapter02 = Chapter.objects.create(
            title="Test Chapter 02-01", serial=0, parent_translation=self.translation02
        )

    def set_user(self, user):
        self.current_user = user
        self.client.force_authenticate(user=user)

    def set_url(self, url):
        self.url = url

    def set_query_params(self, query_params):
        self.query_params = query_params

    def assertReseponseOk(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def assertResponseCreated(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def assertResponseForbidden(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

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

    def call_patch_method(self, data):
        self.response = self.client.patch(
            self.url,
            data,
            format=self.format or "json",
            content_type=self.content_type,
            **self.build_request()
        )
        self.response_json = self.response.json()
        return self.response_json
