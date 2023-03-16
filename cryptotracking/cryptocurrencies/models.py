from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Cryptocurrency(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название'
    )
    symbol = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Символьный код'
    )
    price = models.FloatField(
        verbose_name='Цена за единицу в USD'
    )
    percent_change_24h = models.FloatField(
        verbose_name='Изменение цены в процентах'
    )
    volume = models.FloatField(
        verbose_name='Объем торгов'
    )

    class Meta:
        verbose_name = 'Криптовалюта'
        verbose_name_plural = 'Криптовалюты'

    def __str__(self):
        return self.name, self.symbol, self.price


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    favorite_currency = models.ForeignKey(
        Cryptocurrency,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранные'

    def __str__(self):
        return f'{self.user} --- {self.favorite_currency}'
