from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel
from server.apps.telegram_pay.services.enum import (
    PaymentCurrency,
    PaymentStatus,
)


class Subscription(AbstractModel):
    """Подписка."""

    client = models.ForeignKey(
        to='telegram_clean_prediction.Client',
        verbose_name=_('Клиент'),
        on_delete=models.SET_NULL,
        related_name='subscription',
        null=True,
    )
    expired_at = models.DateTimeField(
        verbose_name=_('Срок действия подписки'),
        auto_now=True,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')

    def __str__(self):
        return self.client
