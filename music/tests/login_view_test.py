from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.views import status

from MusicApi.settings import SIMPLE_JWT
from music.tests.base_view_test import BaseViewTest
from jwt import decode


class LoginViewTest(BaseViewTest):
    def test_should_get_token(self):
        user = User.objects.first()
        response = self.login(user.username, "1234qwer")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])
        self.assertIsNotNone(response.data["refresh"])
        decoded = (decode(response.data["access"], SIMPLE_JWT['SIGNING_KEY'], SIMPLE_JWT['ALGORITHM']))
        self.assertEqual(decoded["user_id"], user.id)
