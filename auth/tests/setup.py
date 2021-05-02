from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

class TestSetup(APITestCase):
    def setUp(self):
        self.register = reverse("register")
        self.login = reverse("login")

        self.data = {
            "email": "email@test.com",
            "username": "email",
            "password": "12345678"
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
