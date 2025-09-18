from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from coin_app.models import CoinInfo, CoinsData
from drf_application.utils.jwt_custom import generate_access_token, generate_refresh_token

class CoinInfoViewSetTests(APITestCase):
    def setUp(self):
        self.coin = CoinInfo.objects.create(name="Bitcoin", foundation_year=2009)

    def test_coininfo_list(self):
        client = APIClient()
        response = client.get("/drf_api/coin_info/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_coininfo_detail(self):
        client = APIClient()
        response = client.get(f"/drf_api/coin_info/{self.coin.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Bitcoin")


class CoinsDataViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@test.com", password="pass1234")
        self.token = generate_access_token(self.user.id)
        self.coindata = CoinsData.objects.create(Name="Ethereum", coin_info=None)

    def test_coinsdata_unauthorized(self):
        client = APIClient()
        response = client.get("/drf_api/coin_data/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_coinsdata_authorized(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get("/drf_api/coin_data/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@mail.com", password="12345")

    def test_obtain_token_valid(self):
        client = APIClient()
        response = client.post("/drf_api/api/custom/token/", {"email": "user1@mail.com", "password": "12345"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_refresh_token(self):
        refresh = generate_refresh_token(self.user.id)
        client = APIClient()
        response = client.post("/drf_api/api/custom/token/refresh/", {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())


class ProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user2", email="user2@mail.com", password="12345")
        self.token = generate_access_token(self.user.id)

    def test_profile_unauthorized(self):
        client = APIClient()
        response = client.get("/drf_api/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authorized(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get("/drf_api/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], "user2@mail.com")