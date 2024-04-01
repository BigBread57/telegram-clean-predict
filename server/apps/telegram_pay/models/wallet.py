import decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel
from server.apps.telegram_pay.services.enum import (
    PaymentCurrency,
    PaymentStatus,
)


class Wallet(AbstractModel):
    """Кошелек."""

    client = models.OneToOneField(
        to='telegram_clean_prediction.Client',
        verbose_name=_('Клиент'),
        on_delete=models.SET_NULL,
        related_name='wallet',
        null=True,
    )
    amount_rub = models.DecimalField(
        verbose_name=_('Количество рублей'),
        max_digits=6,
        decimal_places=2,
        default=decimal.Decimal(0),
    )
    amount_ton = models.DecimalField(
        verbose_name=_('Количество ton'),
        max_digits=6,
        decimal_places=2,
        default=decimal.Decimal(0),
    )
    amount_usdt = models.DecimalField(
        verbose_name=_('Количество usdt'),
        max_digits=6,
        decimal_places=2,
        default=decimal.Decimal(0),
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Кошелек пользователя')
        verbose_name_plural = _('Кошельки пользователей')

    def __str__(self):
        return self.client
