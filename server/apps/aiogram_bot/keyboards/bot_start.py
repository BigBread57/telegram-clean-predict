from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

bot_start_keyboard = InlineKeyboardBuilder()

bot_start_keyboard.row(
    InlineKeyboardButton(
        text='Сделать расклад',
        callback_data='layout_section',
    ),
)
bot_start_keyboard.row(
    InlineKeyboardButton(
        text='Назначение бота',
        callback_data='bot_assignment_section',
    ),
)
bot_start_keyboard.row(
    InlineKeyboardButton(
        text='О нас',
        callback_data='about_us_section',
    ),
)
