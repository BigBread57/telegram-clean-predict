from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

narrating_client_keyboard = InlineKeyboardBuilder()


narrating_client_keyboard.row(
    InlineKeyboardButton(
        text='Пропустить',
        callback_data='skip_section',
    ),
)
