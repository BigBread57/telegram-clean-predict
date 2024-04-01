from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from server.apps.aiogram_bot.keyboards.dialog import dialog_reply_keyboard
from server.apps.aiogram_bot.keyboards.search_dialog import (
    search_dialog_keyboard,
)
from server.apps.aiogram_bot.services.logic_listening_client import (
    LogicListeningClient,
)

router = Router()


@router.callback_query(F.data == 'listening_client_section')
async def listening_client_section(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    """Раздел пользователя, который хочет слушать других пользователей."""
    state_data = await state.get_data()
    client = state_data['client']
    logic_listening_client = LogicListeningClient(client=client)
    await callback.message.edit_text(
        text=(
            'Ожидайте, скоро кому нибудь выслушаете...'
        ),
        reply_markup=search_dialog_keyboard.as_markup(resize_keyboard=True),
    )
    # Поиск рассказчика.
    await logic_listening_client.narrator_search()

    await callback.message.edit_text(
        text=(
            'Вы нашли пользователя! Приятного общения!'
        ),
        reply_markup=dialog_reply_keyboard.as_markup(resize_keyboard=True),
    )
