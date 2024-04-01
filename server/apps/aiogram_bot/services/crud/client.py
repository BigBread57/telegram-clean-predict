from aiogram.types import User

from server.apps.telegram_clean_prediction.models import Client


async def get_client(tg_user_id: int) -> Client:
    """Получение клиента"""
    return await Client.objects.select_related(
        'profile',
        'statistics',
    ).prefetch_related(
        'profile__topics',
    ).aget(tg_user_id=tg_user_id)


async def update_or_create_client(tg_user: User) -> int:
    """Создание или обновление пользователя."""
    client, _ = await Client.objects.aupdate_or_create(
        tg_user_id=tg_user.id,
        defaults={
            'tg_user_username':
                tg_user.username if tg_user.username else '',
            'tg_user_first_name':
                tg_user.first_name if tg_user.first_name else '',
            'tg_user_last_name':
                tg_user.last_name if tg_user.last_name else '',
            'tg_user_language_code':
                tg_user.language_code if tg_user.language_code else '',
            'tg_user_is_premium':
                tg_user.is_premium if tg_user.is_premium else False,
        }
    )

    return client.id
