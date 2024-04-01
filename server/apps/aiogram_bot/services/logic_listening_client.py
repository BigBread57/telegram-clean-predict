import asyncio

from server.apps.aiogram_bot.services.crud.client import get_client
from server.apps.telegram_clean_prediction.models import Client
from server.apps.telegram_clean_prediction.models.dialog import Dialog
from server.apps.telegram_clean_prediction.services.enum import ClientActivity


class LogicListeningClient(object):
    """Логика пользователя, который хочет что-то рассказать."""

    def __init__(self, client: Client) -> None:
        """Инициализация переменных."""
        self.client = client

    async def narrator_search(self) -> None:
        """Поиск рассказывающего."""
        # Статус пользователя меняется на "Поиск рассказывающего"
        self.client.activity = ClientActivity.NARRATOR_SEARCH
        await self.client.asave(update_fields=['activity'])

        # Активность слушателя меняется в LogicNarratingClient.
        while not await self.client.listening_clients.filter(is_active=True).aexists():
            await asyncio.sleep(10)
            await self.client.arefresh_from_db()
