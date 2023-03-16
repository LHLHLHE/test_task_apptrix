import os

from rest_framework.views import APIView

API_KEY = os.getenv('COIN_MARKET_CAP_API_KEY')


class CurrencyListAPIView(APIView):
    pass
