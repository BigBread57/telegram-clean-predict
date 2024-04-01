from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

search_dialog_keyboard = InlineKeyboardBuilder()


search_dialog_keyboard.row(
    InlineKeyboardButton(
        text='Отменить поиск',
        callback_data='cancel_search_dialog_section',
    ),
)
