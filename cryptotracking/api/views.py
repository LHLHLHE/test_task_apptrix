import json
import os

from dotenv import load_dotenv
from requests import Session, Timeout, TooManyRedirects
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv()

API_KEY = os.getenv('COIN_MARKET_CAP_API_KEY')
API_URL = 'https://pro-api.coinmarketcap.com/v1'

HEADERS = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': f'{API_KEY}',
}


def find_by_key(data, symbol):
    for currency_data in data:
        if currency_data['symbol'] == symbol:
            return currency_data


class CurrencyListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        parameters = {'convert': 'USD'}

        session = Session()
        session.headers.update(HEADERS)

        try:
            response = session.get(
                API_URL+'/cryptocurrency/listings/latest',
                params=parameters
            )
            data = find_by_key(json.loads(response.text)['data'], 'FET')
            # data = json.loads(response.text)['data']
            return Response(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({'error': e})
