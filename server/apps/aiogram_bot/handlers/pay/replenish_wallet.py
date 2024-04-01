from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.handlers import PreCheckoutQueryHandler

from server.apps.aiogram_bot.keyboards.pay.replenish_wallet import (
    replenish_wallet_keyboard,
)
from server.apps.aiogram_bot.keyboards.pay.replenishment_methods import (
    replenishment_methods_keyboard,
)

router = Router()


class FSMReplenishWallet(StatesGroup):
    """Класс конечных автоматов для пополнения кошелька."""

    enter_amount = State()


@router.callback_query(F.data == 'replenish_wallet')
async def replenish_wallet(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    """Пополнение кошелька."""
    await state.set_state(state=FSMReplenishWallet.enter_amount)
    await callback.message.edit_text(
        text=(
            'Укажите количество денежных средств для внесения '
        ),
        reply_markup=replenish_wallet_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(FSMReplenishWallet.enter_amount)
async def process_enter_amount(
    message: types.Message,
    state: FSMContext,
):
    """"""
    await state.update_data(amount=message.text)
    await message.answer(
        text='Укажите способ внесения денежных средств ',
        reply_markup=replenishment_methods_keyboard.as_markup(resize_keyboard=True),
    )


# @router.message(FSMReplenishWallet.enter_replenishment_methods)
# async def process_enter_replenishment_methods(
#     callback: types.CallbackQuery,
#     state: FSMContext,
# ):
#     """Раздел поиска групп."""
#     state_data = await state.get_data()
#     await state.set_state(FSMReplenishWallet.enter_replenishment_methods)
#     await callback.message.edit_text(
#         text='Спасибо',
#     )


