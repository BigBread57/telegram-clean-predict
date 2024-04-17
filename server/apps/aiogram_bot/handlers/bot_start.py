from aiogram import F, Router, types
from aiogram.filters import Command

from server.apps.aiogram_bot.keyboards.bot_start import bot_start_keyboard

router = Router()


@router.message(Command(commands=['start']))
async def start(
    message: types.Message,
):
    """
    Приветственное слово.

    Происходит создание клиента и его профиля.
    """
    await message.answer(
        text=(
            'Не можешь решить вопрос?\n'
            'Надоело подбрасывание монеток?\n'
            'Хочешь чего то четкого и ясного?\n'
            'Сделай расклад, все ответы - в пару кликов!'
        ),
        reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
    )


@router.callback_query(F.data == 'bot_assignment_section')
async def bot_assignment_section(
    callback: types.CallbackQuery,
):
    """Раздел назначение бота."""
    await callback.message.edit_text(
        text=(
            'Бот предназначен для получения информацию от вселенной, которая '
            'позволить принять верное решение\n'
        ),
        reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
    )


@router.callback_query(F.data == 'about_us_section')
async def about_us_section(
    callback: types.CallbackQuery,
):
    """Раздел о нас."""
    await callback.message.edit_text(
        text=(
            'Хочется сделать что-то хорошее и полезное для Вас.\n'
            'Пишите @your_clean_support, будем рады любой обратной связи.'
        ),
        reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
    )
