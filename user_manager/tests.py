from django.urls import reverse
from rest_framework.authtoken.models import Token

from helpers.test import TranslationSiteBaseTestCase
from user_manager.models import User


class UserManagerAPITestCase(TranslationSiteBaseTestCase):
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
