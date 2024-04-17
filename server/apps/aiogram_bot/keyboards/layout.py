import math
from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings

layout_keyboard = InlineKeyboardBuilder()


# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Задать конкретный вопрос',
#         callback_data='ask_a_question',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Характеристика человека',
#         callback_data='general_meaning',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Любовь и отношения',
#         callback_data='love_and_relationships',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Работа и карьера',
#         callback_data='work_and_career',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Финансы',
#         callback_data='finance',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Здоровье',
#         callback_data='health',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Ситуация и вопрос',
#         callback_data='situation_and_question',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Карта дня',
#         callback_data='cards_of_the_day',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Совет',
#         callback_data='advice_card',
#     ),
# )

skip_keyboard = InlineKeyboardBuilder()


skip_keyboard.row(
    InlineKeyboardButton(
        text='Пропустить',
        callback_data='skip',
    ),
)

area_of_question = [
    'general_meaning',
    'love_and_relationships',
    'work_and_career',
    'finance',
    'health',
    'situation_and_question',
    'cards_of_the_day',
    'advice_card',
]

#
# three_card_layout_keyboard = InlineKeyboardBuilder()
#
# three_card_layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Линейный расклад',
#         callback_data='advice_card',
#     ),
# )
#
# three_card_layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Сбалансированный расклад',
#         callback_data='advice_card',
#     ),
# )
#
# three_card_layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Перекрещенный расклад',
#         callback_data='advice_card',
#     ),
# )
#
# three_card_layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Фундаментальный расклад',
#         callback_data='advice_card',
#     ),
# )
#
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Быстрый расклад по одной карте',
#         callback_data='one_card_layout_section',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Расклад по трем картам',
#         callback_data='three_card_layout_section',
#     ),
# )
# layout_keyboard.row(
#     InlineKeyboardButton(
#         text='Другие виды раскладов',
#         callback_data='other_layout_section',
#     ),
# )


def get_layout_for_page(
    left_diff: int,
    right_diff: int,
) -> List[InlineKeyboardButton]:
    """Получить темы для конкретной страницы."""
    buttons = []
    for layout in area_of_question[left_diff:right_diff]:
        buttons.append(
            InlineKeyboardButton(
                text='layout',
                callback_data=layout,
            ),
        )

    return buttons



def get_right_button_for_pagination(
    right: int,
    amount_pages: int,
) -> List[InlineKeyboardButton]:
    """Получение правых кнопок для пагинации."""
    return [
        InlineKeyboardButton(
            text="→",
            callback_data=f'pagination {right}',
        ),
        InlineKeyboardButton(
            text="→→",
            callback_data=f'pagination {amount_pages}',
        ),
    ]


def get_left_button_for_pagination(
    left: int,
) -> List[InlineKeyboardButton]:
    """Получение левых кнопок для пагинации."""
    return [
        InlineKeyboardButton(
            text="←←",
            callback_data=f'pagination {1}',
        ),
        InlineKeyboardButton(
            text="←",
            callback_data=f'pagination {left}',
        ),
    ]


def get_center_button_for_pagination(
    page: int,
    amount_pages: int,
) -> InlineKeyboardButton:
    """Получить центральную кнопку для пагинации."""
    return InlineKeyboardButton(
        text=f"{str(page)}/{str(amount_pages)}",
        callback_data='_',
    )


async def get_layout_keyboard(page: int) -> InlineKeyboardBuilder:
    """Получить кнопки для названия тем, которые указал пользователь."""
    topic_keyboard = InlineKeyboardBuilder()
    amount_pages = math.ceil(
        len(area_of_question) / settings.AMOUNT_OBJECT_IN_PAGE,
    )
    left = page - 1 if page != 1 else 1
    right = page + 1 if page != amount_pages else amount_pages

    # Если страница равна первой странице, то не рисуем кнопки влево.
    # Если страница равна последней странице, то не рисуем кнопки вправо.
    # В других случаях рисуем все кнопки.
    if page == 1:
        topic_keyboard.row(
            *get_layout_for_page(
                left_diff=0,
                right_diff=settings.AMOUNT_OBJECT_IN_PAGE,
            ),
            width=1,
        )
        topic_keyboard.row(
            get_center_button_for_pagination(
                page=page,
                amount_pages=amount_pages,
            ),
            *get_right_button_for_pagination(
                right=right,
                amount_pages=amount_pages,
            ),
        )

    else:
        topic_keyboard.row(
            *get_layout_for_page(
                left_diff=(page - 1) * settings.AMOUNT_OBJECT_IN_PAGE,
                right_diff=page * settings.AMOUNT_OBJECT_IN_PAGE,
            ),
            width=1,
        )

        if page == amount_pages:
            topic_keyboard.row(
                *get_left_button_for_pagination(
                    left=left,
                ),
                get_center_button_for_pagination(
                    page=page,
                    amount_pages=amount_pages,
                ),
            )
        else:
            topic_keyboard.row(
                *get_left_button_for_pagination(
                    left=left,
                ),
                get_center_button_for_pagination(
                    page=page,
                    amount_pages=amount_pages,
                ),
                *get_right_button_for_pagination(
                    right=right,
                    amount_pages=amount_pages,
                ),
            )

    return topic_keyboard
