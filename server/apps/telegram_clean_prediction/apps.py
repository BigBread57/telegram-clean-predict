from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TelegramSearchConfig(AppConfig):
    """Конфиг приложения "Поисковик"."""

    name = 'server.apps.telegram_clean_prediction'
    verbose_name = _('Поисковик')

    def ready(self) -> None:
        """Подключение прав происходит при подключении app."""
        import server.apps.telegram_clean_prediction.api.routers
        import server.apps.telegram_clean_prediction.permissions
