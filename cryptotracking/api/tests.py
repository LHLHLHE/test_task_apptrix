from django.test import RequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .views import CurrencyListAPIView, CurrencyRetrieveAPIView
from cryptocurrencies.models import Favorites, Cryptocurrency, User


class TestCurrencyListAPIView(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = CurrencyListAPIView.as_view()

    def test_get_currency_list(self):
        request = self.factory.get('/api/currencies/')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

    def test_get_currency_list_with_params(self):
        convert = 'EUR'
        request = self.factory.get(f'/api/currencies?convert={convert}')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(list(response.data[0]['quote'])[0], convert)

    def test_search_currency(self):
        symbol = 'ETH'
        request = self.factory.get(f'/api/currencies?symbol={symbol}')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['symbol'], symbol)


class TestCurrencyRetrieveAPIView(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = CurrencyRetrieveAPIView.as_view()

    def test_get_currency(self):
        symbol = 'ETH'
        request = self.factory.get(f'/api/currencies/{symbol}/')
        response = self.view(request, symbol)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(response.data['symbol'], symbol)

    def test_get_currency_with_params(self):
        convert = 'EUR'
        symbol = 'ETH'
        request = self.factory.get(
            f'/api/currencies/{symbol}?convert={convert}'
        )
        response = self.view(request, symbol)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(list(response.data['quote'])[0], convert)


class FavoritesCreateDestroyAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        cls.token = cls.token = Token.objects.create(user=cls.user)

        cls.client = APIClient()

        cls.symbol = 'BTC'
        cls.url = f'/api/currencies/{cls.symbol}/favorite/'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_create_favorite(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Cryptocurrency.objects.filter(symbol=self.symbol).exists()
        )
        self.assertTrue(Favorites.objects.filter(
            user=self.user,
            favorite_currency__symbol=self.symbol
        ).exists())

    def test_create_existing_favorite(self):
        Favorites.objects.create(
            user=self.user,
            favorite_currency=Cryptocurrency.objects.create(
                name='Bitcoin',
                symbol=self.symbol
            )
        )
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_favorite(self):
        Favorites.objects.create(
            user=self.user,
            favorite_currency=Cryptocurrency.objects.create(
                name='Bitcoin',
                symbol=self.symbol
            )
        )
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorites.objects.filter(
            user=self.user,
            favorite_currency__symbol=self.symbol
        ).exists())


class FavoritesListAPIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        cls.symbol = 'BTC'
        Favorites.objects.create(
            user=cls.user,
            favorite_currency=Cryptocurrency.objects.create(
                name='Bitcoin',
                symbol=cls.symbol
            )
        )
        cls.token = cls.token = Token.objects.create(user=cls.user)

        cls.client = APIClient()

        cls.url = f'/api/currencies/favorites/'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_get_favorites(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

    def test_get_favorites_with_params(self):
        convert = 'EUR'
        response= self.client.get(self.url + f'?convert={convert}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertTrue(response.data[self.symbol][0]['quote'].get(convert))
