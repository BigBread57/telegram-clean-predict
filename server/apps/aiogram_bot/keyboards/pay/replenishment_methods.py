from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

replenishment_methods_keyboard = InlineKeyboardBuilder()

replenishment_methods_keyboard.row(
    InlineKeyboardButton(
        text='Телеграм',
        callback_data='replenishment_via_telegram',
    ),
)
replenishment_methods_keyboard.row(
    InlineKeyboardButton(
        text='ЮКасса',
        callback_data='replenishment_via_ykassa',
    ),
)
replenishment_methods_keyboard.row(
    InlineKeyboardButton(
        text='TON',
        callback_data='replenishment_via_toncoin',
    ),
)
replenishment_methods_keyboard.row(
    InlineKeyboardButton(
        text='USDT',
        callback_data='replenishment_via_usdt',
    ),
)
