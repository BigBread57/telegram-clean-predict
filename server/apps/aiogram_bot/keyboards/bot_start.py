from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from server.apps.aiogram_bot.keyboards.layout import LayoutCallback

bot_start_keyboard = InlineKeyboardBuilder()

bot_start_keyboard.row(
    InlineKeyboardButton(
        text='Расклад',
        callback_data=LayoutCallback(is_back=False).pack(),
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


# back_keyboard = InlineKeyboardBuilder()
#
# back_keyboard.row(
#     InlineKeyboardButton(
#         text='Назад',
#         callback_data=ProfileSectionCallback(is_back=True).pack(),
#     ),
# )
