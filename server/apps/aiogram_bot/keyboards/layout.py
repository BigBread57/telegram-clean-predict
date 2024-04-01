from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class LayoutCallback(CallbackData, prefix='layout_callback'):
    """Класс для расклада."""

    key: str = 'layout_section'
    value: str = 'расклад'


layout_keyboard = InlineKeyboardBuilder()


layout_keyboard.row(
    InlineKeyboardButton(
        text='расклад с одной картой',
        callback_data='one_card',
    ),
)
