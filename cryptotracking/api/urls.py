from django.urls import path, include, re_path

from .views import (
    CurrencyRetrieveAPIView,
    CurrencyListAPIView,
    FavoritesCreateDestroyAPIView,
    FavoritesListAPIView,
    NewsAPIView
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('news/', NewsAPIView.as_view(), name='news'),
    path(
        'currencies/',
        CurrencyListAPIView.as_view(),
        name='currency_list'
    ),
    re_path(
        r'currencies/(?P<currency_symbol>[0-9]*[A-Z]+)/$',
        CurrencyRetrieveAPIView.as_view(),
        name='currency'
    ),
    re_path(
        r'currencies/(?P<currency_symbol>[0-9]*[A-Z]+)/favorite',
        FavoritesCreateDestroyAPIView.as_view(),
        name='add_delete_favorites'
    ),
    path(
        'currencies/favorites/',
        FavoritesListAPIView.as_view(),
        name='get_favorites'
    ),
    path('', include('djoser.urls.base')),
]
