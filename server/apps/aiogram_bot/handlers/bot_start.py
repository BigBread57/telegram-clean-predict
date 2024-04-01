from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from server.apps.aiogram_bot.keyboards.bot_start import bot_start_keyboard

router = Router()


@router.message(Command(commands=['start']))
async def start(
    message: types.Message,
):
    """Приветственное слово.

    Происходит создание клиента и его профиля.
    """
    await message.answer(
        text=(
            'Не можешь решить вопрос? Надоело подбрасывание монеток? '
            'Хочешь чего то четкого и ясного? Сделай расклад, все ответы -'
            'в пару кликов!'
        ),
        reply_markup=bot_start_keyboard.as_markup(resize_keyboard=True),
    )


@router.callback_query(F.data == 'main_menu_section')
async def main_menu_section(
    callback: types.CallbackQuery,
):
    """Главное меню.

    Используется, когда пользователь нажимает главное меню во время
    использования бота. Возвращает стартовое состояние бота.
    """
    await callback.message.edit_text(
        text=(
            'Выберите необходимый пункт меню:'
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
            'Цели бота:\n'
            '1) Вы можете делиться своими переживаниями, трудностями или '
            'мыслями с другим человеком.\n'
            '2) Вы можете оказывать поддержку другим людям, выслушав и '
            'поддержав их\n'
            '3) Возможность получения реальных советов и поддержки для '
            'решения возникших ситуаций в вашей жизни\n'
            '4) Экономия денежных средств на посещение психологов\n\n'
            'Особенности бота:\n'
            '1) Бот не хранит ваши сообщения, историю сообщений хранит только '
            'Telegram.\n'
            '2) Анонимные сообщения от реальных людей. Ни вы ни ваш собеседник '
            'не узнает с кем происходит общается.\n'
            '3) Система жалоб позволяет общаться с адекватными людьми, получать'
            'реальную поддержку и советы.\n'
            '4) Система поиска собеседника по интересующим вас темам.'


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
