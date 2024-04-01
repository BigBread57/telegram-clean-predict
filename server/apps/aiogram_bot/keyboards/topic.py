import math
from typing import List, Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings

from server.apps.aiogram_bot.keyboards.profile import ProfileSectionCallback
from server.apps.aiogram_bot.services.crud.topic import topic_storage


def get_topic_for_page(
    left_diff: int,
    right_diff: int,
    client_topic_keys: Optional[List[str]] = None,
) -> List[InlineKeyboardButton]:
    """Получить темы для конкретной страницы."""
    buttons = []
    for topic in topic_storage.topics[left_diff:right_diff]:
        if client_topic_keys and topic.key in client_topic_keys:
            buttons.append(
                InlineKeyboardButton(
                    text=f'✅ {topic.name}',
                    callback_data=topic.key,
                ),
            )
        else:
            buttons.append(
                InlineKeyboardButton(
                    text=topic.name,
                    callback_data=topic.key,
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


async def get_topic_keyboard(
    page: int,
    client_topic_keys: Optional[List[str]] = None,
) -> InlineKeyboardBuilder:
    """Получить кнопки для названия тем, которые указал пользователь."""
    topic_keyboard = InlineKeyboardBuilder()
    amount_pages = math.ceil(
        topic_storage.amount / settings.AMOUNT_TOPIC_IN_PAGE,
    )
    left = page - 1 if page != 1 else 1
    right = page + 1 if page != amount_pages else amount_pages

    # Если страница равна первой странице, то не рисуем кнопки влево.
    # Если страница равна последней странице, то не рисуем кнопки вправо.
    # В других случаях рисуем все кнопки.
    if page == 1:
        topic_keyboard.row(
            *get_topic_for_page(
                left_diff=0,
                right_diff=settings.AMOUNT_TOPIC_IN_PAGE,
                client_topic_keys=client_topic_keys,
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
            *get_topic_for_page(
                left_diff=(page - 1) * settings.AMOUNT_TOPIC_IN_PAGE,
                right_diff=page * settings.AMOUNT_TOPIC_IN_PAGE,
                client_topic_keys=client_topic_keys,
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

    if client_topic_keys:
        topic_keyboard.row(
            InlineKeyboardButton(
                text='Сохранить темы',
                callback_data='save_topics',
            ),
        )
        topic_keyboard.row(
            InlineKeyboardButton(
                text='Назад',
                callback_data=ProfileSectionCallback(is_back=True).pack(),
            ),
        )
    else:
        topic_keyboard.row(
            InlineKeyboardButton(
                text='Отменить поиск',
                callback_data='cancel_search_dialog_section',
            ),
        )

    return topic_keyboard
