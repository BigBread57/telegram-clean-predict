from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from server.apps.telegram_pay.models import TariffPlan


async def get_tariff_plan_keyboard() -> InlineKeyboardBuilder:
    """Получить виды тарифных планов."""
    tariff_plans_keyboard = InlineKeyboardBuilder()
    async for tariff_plan in TariffPlan.objects.filter(is_actual=True):
        tariff_plans_keyboard.row(
            InlineKeyboardButton(
                text=tariff_plan.title,
                callback_data=tariff_plan.key,
            ),
        )
    tariff_plans_keyboard.row(
        InlineKeyboardButton(
            text='Подробнее',
            callback_data='about_tariff_plan',
        ),
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='main_menu_section',
        ),
    )
    return tariff_plans_keyboard
