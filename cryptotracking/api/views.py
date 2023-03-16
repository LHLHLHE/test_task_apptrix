import json
import os

from dotenv import load_dotenv
from requests import Session, Timeout, TooManyRedirects
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv()

API_KEY = os.getenv('COIN_MARKET_CAP_API_KEY')
API_URL = 'https://pro-api.coinmarketcap.com'

HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': f'{API_KEY}',
}


class CurrencyListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'index.html'

    def get(self, request):
        session = Session()
        session.headers.update(HEADERS)

        params = request.query_params

        try:
            response = session.get(
                API_URL + '/v1/cryptocurrency/listings/latest',
                params=params
            )
            data = json.loads(response.text).get('data')
            return Response({'data': data, 'convert': params.get('convert')})
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({'error': e})


class CurrencyRetrieveAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, currency_symbol):
        parameters = {
            'symbol': currency_symbol
        } | request.query_params

        session = Session()
        session.headers.update(HEADERS)

        try:
            response = session.get(
                API_URL+'/v2/cryptocurrency/quotes/latest',
                params=parameters
            )
            data = json.loads(response.text).get('data')
            return Response(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({'error': e})


# class AddToFavoritesAPIView(APIView):
#     def post(self, request, currency_symbol):

