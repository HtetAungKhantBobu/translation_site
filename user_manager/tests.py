from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user_manager.models import User


class UserManagerAPITestCase(APITestCase):
    def setUp(self):
        self.url = None
        self.format = None
        self.content_type = None
        self.http_origin = None
        self.query_params = None
        self.response = None
        self.response_json = None

        self.normal_user = User.objects.create_user(email="testuser01@gmail.com")
        self.superuser = User.objects.create_superuser(
            email="testsuperuser01@gmail.com", password="testpw"
        )
        self.superuser.save()

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

    def test_user_registration(self):
        data = {
            "email": "testuser02@gmail.com",
            "password": "test",
            "password2": "test",
            "name": "Test User 02",
        }
        self.set_url(reverse("v1:auth-register"))
        self.call_post_method(data=data)
        self.assertResponseCreated()

        user = User.objects.get(email="testuser02@gmail.com")
        self.assertEqual(self.response_json["id"], str(user.id))
        self.assertEqual(self.response_json["name"], user.name)
        self.assertTrue(self.response_json["is_active"])

    def test_user_login(self):
        data = {"email": self.superuser.email, "password": "testpw"}
        self.set_url(reverse("v1:auth-login"))
        self.call_post_method(data=data)
        self.assertReseponseOk()
        token = Token.objects.get(user=self.superuser)
        self.assertEqual(self.response_json["token"], str(token))
