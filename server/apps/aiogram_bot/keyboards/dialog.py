from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

dialog_reply_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Пожаловаться на собеседника')],
        [types.KeyboardButton(text='Завершить диалог')],
    ],
)

end_dialog_reply_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Завершить диалог')],
    ],
)

dialog_keyboard = InlineKeyboardBuilder()

dialog_keyboard.row(
    InlineKeyboardButton(
        text='Отправить сообщения на проверку',
        callback_data='send_message_for_review_section',
    ),
    InlineKeyboardButton(
        text='Отменить подачу жалобы.',
        callback_data='cancellation_complaint_section',
    ),
)
