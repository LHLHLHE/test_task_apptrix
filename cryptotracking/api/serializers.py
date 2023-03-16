from rest_framework import serializers


class CurrencyGetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    symbol = serializers.CharField(max_length=3)

