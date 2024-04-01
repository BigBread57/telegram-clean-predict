from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TelegramPaymentConfig(AppConfig):
    """Конфиг приложения "Оплата"."""

    name = 'server.apps.telegram_pay'
    verbose_name = _('Оплата')
