from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from users.models import User


class TestPlanos(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com',
            'password1'
        )
        self.token = Token.objects.create(user=self.writer)


class TestPlanosListView(TestPlanos):
    def test_liste_planos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get("/planos/liste")
        self.assertEqual(response.status_code, 200)
