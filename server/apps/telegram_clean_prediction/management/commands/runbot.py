import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from django.core.management.base import BaseCommand

from server.apps.aiogram_bot.bot import aiogram_bot
from server.apps.aiogram_bot.handlers import (
    bot_start,
    layout,
)
# from server.apps.aiogram_bot.handlers.pay import (
#     replenish_wallet,
#     replenishment_methods,
#     tariff_plan,
# )
from server.apps.aiogram_bot.middleware.check_privileges import (
    CheckPrivilegesMiddleware,
)


async def on_startup():
    """Запуск бота."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    dp = Dispatcher(storage=MemoryStorage())
    # dp.callback_query.middleware(CheckPrivilegesMiddleware())
    # dp.message.middleware(CheckPrivilegesMiddleware())
    dp.include_router(bot_start.router)
    dp.include_router(layout.router)
    # dp.include_router(replenish_wallet.router)
    # dp.include_router(replenishment_methods.router)
    # dp.include_router(tariff_plan.router)

    await dp.start_polling(aiogram_bot)


class Command(BaseCommand):
    """Команда для запуска телеграм бота."""
    help = 'python manage.py runbot'

    def handle(self, *args, **options):
        """Запуск бота."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(on_startup())
