from aiogram.fsm.context import FSMContext

from server.apps.telegram_clean_prediction.models import Client


async def state_clear(state: FSMContext, state_data: dict):
    """Очистка state."""
    await state.set_state(state=None)
    await state.set_data(
        {'tg_user_id': state_data.get('tg_user_id', '')},
    )
