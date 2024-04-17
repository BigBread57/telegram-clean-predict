from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from server.apps.aiogram_bot.services.crud.client import (
    update_or_create_client,
)
from server.apps.telegram_clean_prediction.models import Client
from server.apps.telegram_clean_prediction.services.enum import (
    ClientPrivileges,
)


class CheckPrivilegesMiddleware(BaseMiddleware):
    """Проверка привилегий у пользователя."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        """Проверка привилегий у пользователя."""
        text = 'Вы имеете ограничения на использование бота'
        state_data = await data['state'].get_data()
        if client := state_data.get('client'):
            if client.privileges == ClientPrivileges.MISSING:
                await event.answer(text)
                return None
        else:
            client = await update_or_create_client(tg_user=event.from_user)
            if client.privileges == ClientPrivileges.MISSING:
                await event.answer(text)
                return None

            await data['state'].update_data(client=client)

        return await handler(event, data)
