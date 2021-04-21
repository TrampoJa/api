from django.test import TestCase
from users.views import User
from django.test.client import Client
from django.http import *

class TestIndex(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get("//")
        self.assertEqual(response.status_code, 200)