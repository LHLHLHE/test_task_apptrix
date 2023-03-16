from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.base')),
]
