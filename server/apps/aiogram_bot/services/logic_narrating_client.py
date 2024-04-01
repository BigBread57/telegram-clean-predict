import asyncio
from typing import Optional

from django.db import models

from server.apps.telegram_clean_prediction.models import Client, Topic
from server.apps.telegram_clean_prediction.models.dialog import Dialog
from server.apps.telegram_clean_prediction.services.enum import ClientActivity


class LogicNarratingClient(object):
    """Логика пользователя, который хочет выслушать."""

    def __init__(
        self,
        client: Client,
        topic_key: str,
        additional_topic: Optional[str] = None,
    ):
        """Инициализация переменных."""
        self.client = client
        self.topic_key = topic_key
        self.additional_topic = additional_topic

    async def create_dialog(self, listener: Client):
        """Создание диалога."""
        topic = await Topic.objects.aget(key=self.topic_key)
        Dialog.objects.acreate(
            narrating_client=self.client,
            listening_client=listener,
            topic=topic,
            additional_topic=self.additional_topic,
        )

    async def listener_search(self) -> int:
        """Поиск клиента, который будет слушать."""
        # Статус пользователя меняется на "поиск слушателя"
        self.client.activity = ClientActivity.LISTENER_SEARCH
        await self.client.asave(update_fields=['activity'])

        # Осуществляем поиск свободных слушателей.
        listener = [
            client
            async for client in Client.objects.filter(
                models.Q(
                    models.Q(profile__topics__key=self.topic_key) |
                    models.Q(profile__additional_topics__icontains=self.additional_topic)  # noqa: E501
                ),
                activity=ClientActivity.NARRATOR_SEARCH,
            )
        ]

        while not listener:
            await asyncio.sleep(5)
            listener = [
                client
                async for client in Client.objects.filter(
                    models.Q(
                        models.Q(profile__topics__key=self.topic_key) |
                        models.Q( profile__additional_topics__icontains=self.additional_topic)  # noqa: E501
                    ),
                    activity=ClientActivity.NARRATOR_SEARCH,
                )
            ]

        listener = listener[0]

        self.client.activity = ClientActivity.ACTIVE
        listener.activity = ClientActivity.ACTIVE
        await self.client.asave(update_fields=['activity'])
        await listener.asave(update_fields=['activity'])
        await self.create_dialog(listener=listener)

        return listener.tg_user_id
