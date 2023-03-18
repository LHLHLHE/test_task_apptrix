import json
import os

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from requests import Session, Timeout, TooManyRedirects
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cryptocurrencies.models import Favorites, Cryptocurrency

load_dotenv()

API_KEY = os.getenv('COIN_MARKET_CAP_API_KEY')
API_URL = 'https://pro-api.coinmarketcap.com'

CURRENCY_LIST_ENDPOINT = '/v1/cryptocurrency/listings/latest'
CURRENCY_ENDPOINT = '/v2/cryptocurrency/quotes/latest'

HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': f'{API_KEY}',
}


class CurrencyListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        endpoint = CURRENCY_LIST_ENDPOINT
        session = Session()
        session.headers.update(HEADERS)

        params = request.query_params.copy()

        search_param = params.get('symbol')

        if search_param:
            endpoint = CURRENCY_ENDPOINT
        try:
            response = session.get(
                API_URL + endpoint,
                params=params
            )
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({'error': e})

        if search_param:
            data = json.loads(response.text).get('data').get(search_param)
        else:
            data = json.loads(response.text).get('data')
        return Response(data, status=status.HTTP_200_OK)


class CurrencyRetrieveAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, currency_symbol):
        parameters = {
            'symbol': currency_symbol
        } | request.query_params

        session = Session()
        session.headers.update(HEADERS)

        user = request.user

        try:
            response = session.get(
                API_URL+'/v2/cryptocurrency/quotes/latest',
                params=parameters
            )
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({'error': e})

        data = json.loads(response.text).get('data').get(currency_symbol)[0]

        data['is_favorite'] = False

        if type(user) != AnonymousUser:
            data['is_favorite'] = Favorites.objects.filter(
                user=user,
                favorite_currency__symbol=currency_symbol
            ).exists()

        return Response(data, status=status.HTTP_200_OK)


class FavoritesCreateDestroyAPIView(APIView):
    def post(self, request, currency_symbol):
        parameters = {
            'symbol': currency_symbol
        }

        session = Session()
        session.headers.update(HEADERS)

        try:
            response = session.get(
                API_URL+'/v2/cryptocurrency/quotes/latest',
                params=parameters
            )
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({'error': e})

        data = json.loads(response.text).get('data')
        user = request.user

        if not Favorites.objects.filter(
                user=user,
                favorite_currency__symbol=currency_symbol
        ).exists():
            currency, created = Cryptocurrency.objects.get_or_create(
                name=data[currency_symbol][0]['name'],
                symbol=currency_symbol
            )
            Favorites.objects.create(
                user=user,
                favorite_currency=currency
            )
            return Response(status=status.HTTP_201_CREATED)

        return Response(
            {'error': 'Криптовалюта уже в избранном'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, currency_symbol):
        user = request.user

        get_object_or_404(
            Favorites,
            user=user,
            favorite_currency__symbol=currency_symbol
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoritesListAPIView(APIView):
    def get(self, request):
        params = request.query_params.copy()

        user = request.user

        favorites = user.favorites.all()

        symbols = ''

        for favorite in favorites:
            if symbols:
                symbols += ','
            symbols += favorite.favorite_currency.symbol

        params['symbol'] = symbols

        session = Session()
        session.headers.update(HEADERS)

        try:
            response = session.get(
                API_URL + '/v2/cryptocurrency/quotes/latest',
                params=params
            )
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({'error': e})

        data = json.loads(response.text).get('data')

        return Response(data, status=status.HTTP_200_OK)


