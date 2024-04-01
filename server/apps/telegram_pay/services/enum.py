from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentStatus(models.TextChoices):
    """Статус платежа."""

    NEW = 'new', _('Новый')
    SUCCESS = 'success', _('Успех')
    ERROR = 'error', _('Ошибка')


class PaymentCurrency(models.TextChoices):
    """Валюта платежа."""

    RUB = 'rub', _('Рубль')
    TON = 'ton', _('Toncoin')
    USDT = 'usdt', _('Usdt')
