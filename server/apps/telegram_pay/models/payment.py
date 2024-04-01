from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel
from server.apps.telegram_pay.services.enum import (
    PaymentCurrency,
    PaymentStatus,
)


class Payment(AbstractModel):
    """Платеж клиента."""

    client = models.ForeignKey(
        to='telegram_clean_prediction.Client',
        verbose_name=_('Клиент'),
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True,
    )
    status = models.CharField(
        verbose_name=_('Статус платежа'),
        choices=PaymentStatus.choices,
    )
    currency = models.CharField(
        verbose_name=_('Валюта платежа'),
        choices=PaymentCurrency.choices,
    )
    amount = models.DecimalField(
        verbose_name=_('Количество внесенных денежных средств'),
        max_digits=10,
        decimal_places=2,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Платеж клиента')
        verbose_name_plural = _('Платежи клиентов')

    def __str__(self):
        return self.client
