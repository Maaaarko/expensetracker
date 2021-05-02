from .setup import TestSetup
from ..models import User

class TestViews(TestSetup):
    def test_register(self):
        res = self.client.post(self.register, self.data, format="json")
        self.assertEqual(res.data["email"], self.data["email"])
        self.assertEqual(res.data["username"], self.data["username"])
        self.assertEqual(res.status_code, 201)

    def test_verify_login_bypass(self):
        self.client.post(self.register, self.data, format="json")
        res = self.client.post(self.login, self.data, format="json")
        self.assertEquals(res.status_code, 401)

    def test_verify_login(self):
        res = self.client.post(self.register, self.data, format="json")
        email = res.data["email"]
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        
        res = self.client.post(self.login, self.data, format="json")
        self.assertEquals(res.status_code, 200)