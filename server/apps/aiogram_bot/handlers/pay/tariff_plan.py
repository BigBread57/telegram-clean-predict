from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from server.apps.aiogram_bot.keyboards.bot_start import bot_start_keyboard
from server.apps.aiogram_bot.keyboards.pay.replenishment_methods import (
    replenishment_methods_keyboard,
)
from server.apps.aiogram_bot.keyboards.pay.tariff_plan import (
    get_tariff_plan_keyboard,
)

router = Router()


class FSMTariffPlan(StatesGroup):
    """Класс конечных автоматов для оплаты тарифа."""

    enter_tariff_plan = State()


@router.callback_query(F.data == 'tariff_plan')
async def tariff_plan(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    """Раздел оплаты тарифного плана."""
    await state.set_state(state=FSMTariffPlan.enter_tariff_plan)
    tariff_plan_keywords = await get_tariff_plan_keyboard()
    await callback.message.edit_text(
        text=(
            'Выберите тариф'
        ),
        reply_markup=tariff_plan_keywords.as_markup(resize_keyboard=True),
    )


@router.callback_query(FSMTariffPlan.enter_tariff_plan)
async def process_enter_tariff_plan(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    """Выбор тарифного плана для оплаты."""
    await state.update_data(tariff_plan_key=callback.data)
    await callback.message.edit_text(
        text=(
            'Выберите способ оплаты'
        ),
        reply_markup=replenishment_methods_keyboard.as_markup(resize_keyboard=True),
    )


@router.callback_query(F.data == 'about_tariff_plan')
async def about_tariff_plan(
    callback: types.CallbackQuery,
):
    """Подробнее о тарифных планах."""
    await callback.message.edit_text(
        text=(
            'Подробнее о тарифных планах'
        ),
        reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
    )
