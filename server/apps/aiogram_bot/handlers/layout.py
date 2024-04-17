import io

from PIL import Image, ImageEnhance
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, InputMediaPhoto, BufferedInputFile

from server.apps.aiogram_bot.keyboards.layout import layout_keyboard, \
    get_layout_keyboard
from server.apps.aiogram_bot.services.generate_card import (
    generate_card_for_layout, get_answer,
)
from server.apps.telegram_clean_prediction.services.enum import DeckType

router = Router()


class FSMQuestion(StatesGroup):
    """
    Класс конечных автоматов.

    Создание вопроса.
    """

    enter_question = State()


@router.callback_query(F.data == 'layout_section')
async def layout_section_for_callback(
    callback: types.CallbackQuery,
):
    """Выбрать расклад из меню бота."""
    photo = FSInputFile('server/cards/fortune_teller.jpeg')
    topic_keyboard = await get_layout_keyboard(
        page=1,
    )
    await callback.message.answer_photo(
        caption=(
            'Выберите область в которой вы хотите задать вопрос:'
        ),
        photo=photo,
        reply_markup=topic_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(F.text.lower() == 'расклад')
async def layout_section_for_message(
    message: types.Message,
):
    """Выбрать расклад по ключевому слову."""
    photo = FSInputFile('server/cards/fortune_teller.jpeg')
    await message.answer_photo(
        caption=(
            'Выберите область в которой вы хотите задать вопрос:'
        ),
        photo=photo,
        reply_markup=layout_keyboard.as_markup(resize_keyboard=True),
    )


@router.callback_query(F.data == 'ask_a_question')
async def ask_a_question(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    """Конкретный пользовательский вопрос."""
    await state.set_state(FSMQuestion.enter_question)
    await callback.message.edit_caption(
        caption=(
            'Напишите интересующий вас вопрос:\n'
            'Например:\n'
            '- Что мне сделать, чтобы увеличить свои доходы?\n'
            '- Где я могу реализовать свои способности?\n'
            '- Что нужно знать о нынешних отношениях?\n'
        ),
    )


@router.message(FSMQuestion.enter_question)
async def process_enter_question(
    message: types.Message,
):
    """Ввод вопроса, который интересует клиента."""
    user_cards, answer = await get_answer(
        number_of_cards=3,
        deck_type=DeckType.RIDER_WAITE_TAROT,
        question=message.text,
    )


@router.callback_query(
    F.data.in_(
        {
            'general_meaning',
            'love_and_relationships',
            'work_and_career',
            'finance',
            'health',
            'situation_and_question',
            'cards_of_the_day',
            'advice_card',
        },
    ),
)
async def type_layout_section(
    callback: types.CallbackQuery,
):
    """Получение информации о типе расклада."""
    position, card = await generate_card_for_layout(
        number_of_cards=1,
        deck_type=DeckType.RIDER_WAITE_TAROT,
    )


    # new = Image.new("RGBA", (1123, 550))
    # img = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/inverted/1_the_magician.png")
    #
    # new.paste(img, (0,0))
    # new.paste(img, (400,0))
    # new.paste(img, (800,0))
    #
    # new.save('test.png')
    #
    # media_1 = InputMediaPhoto(
    #     media=FSInputFile(f'test.png'),
    #     caption=(
    #         f'Ваша карта: {card.name}\n'
    #         f'{card.description.get(callback.data).get(position)}'
    #     ),
    # )
    #
    # await callback.message.edit_media(
    #     media=media_1,
    #     reply_markup=layout_keyboard.as_markup(resize_keyboard=True),
    # )

    # new = Image.new("RGBA", (1123, 550))
    # img = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/inverted/1_the_magician.png")
    #
    # new.paste(img, (0,0))
    # new.paste(img, (400,0))
    # new.paste(img, (800,0))

    new = Image.new("RGBA", (2000, 2000))

    img = Image.open(
        "/home/gleb/Experience/telegram-clean-prediction/server/cards/inverted/1_the_magician.png")

    new.paste(img.rotate(-45, expand=True), (0, 500))
    new.paste(
        img.transpose(method=Image.FLIP_LEFT_RIGHT).rotate(45, expand=True),
        (700, 500))
    new.paste(img, (500, 0))

    imgByteArr = io.BytesIO()
    # image.save expects a file-like as a argument
    new.save(imgByteArr, format='png')
    # Turn the BytesIO object back into a bytes object
    # return imgByteArr

    media_1 = InputMediaPhoto(
        media=BufferedInputFile(file=imgByteArr.getvalue(), filename='test.png'),
        caption=(
            f'Ваша карта: {card.name}\n'
            f'{card.description.get(callback.data).get(position)}'
        ),
    )

    await callback.message.edit_media(
        media=media_1,
        reply_markup=layout_keyboard.as_markup(resize_keyboard=True),
    )

