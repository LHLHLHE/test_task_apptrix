from django.urls import path, include, re_path

from .views import CurrencyRetrieveAPIView, CurrencyListAPIView

urlpatterns = [
    path('v1/auth/', include('djoser.urls.authtoken')),
    path(
        'v1/currencies/',
        CurrencyListAPIView.as_view(),
        name='currency_list'
    ),
    re_path(
        r'v1/currencies/(?P<currency_symbol>[A-Z]+)',
        CurrencyRetrieveAPIView.as_view(),
        name='currency'
    ),
    path('v1/', include('djoser.urls.base')),
]
