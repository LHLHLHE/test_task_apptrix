from django.urls import path, include

from api.views import CurrencyListAPIView

urlpatterns = [
    path('v1/auth/', include('djoser.urls.authtoken')),
    path(
        'v1/currencies/',
        CurrencyListAPIView.as_view(),
        name='currencies_list'
    ),
    path('v1/', include('djoser.urls.base')),
]
