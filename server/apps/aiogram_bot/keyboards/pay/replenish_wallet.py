from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

replenish_wallet_keyboard = InlineKeyboardBuilder()

replenish_wallet_keyboard.row(
    InlineKeyboardButton(
        text='Главное меню',
        callback_data='main_menu_section',
    ),
)
