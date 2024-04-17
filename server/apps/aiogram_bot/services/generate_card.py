import random
from typing import Optional, Tuple, Dict, Any, List

import asyncstdlib
from openai import OpenAI
from server.apps.telegram_clean_prediction.models import Card
from server.apps.telegram_clean_prediction.services.enum import DeckType

# OPENAI_API_KEY='1234'

# client = OpenAI(api_key=OPENAI_API_KEY)
client = None


async def generate_card_for_layout(
    number_of_cards: int,
    deck_type: str,
) -> List[Card]:
    # Получаем все карты для колоды.
    cards = [
        card
        async for card in Card.objects.filter(deck_type=deck_type)
    ]
    # Перемешиваем все карты для колоды.
    random.shuffle(cards)
    return random.choices(cards, k=number_of_cards)


async def get_answer(
    number_of_cards: int,
    deck_type: str,
    question: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Получение карт для расклада.
    """
    # Переменная для хранения информации о выпавших пользователю картах.
    user_cards = []
    cards_for_layout = await generate_card_for_layout(
        number_of_cards=number_of_cards,
        deck_type=deck_type,
    )
    cards_content = ''
    async for index, card in asyncstdlib.enumerate(cards_for_layout):
        position = card.position
        position_content = (
            ' в перевернутом положении'
            if position == 'inverted'
            else ''
        )
        cards_content += f'№{index + 1} - {card.name}{position_content};'
        user_cards.append({'card': card, 'position': position})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are a tarot reader who is well versed in tarot '
                    'cards, understand the meaning of the cards and '
                    'their relationship with each other'
                ),
            },
            {
                'role': 'user',
                'content': (
                    'Необходимо объяснить расклад карт таро. '
                    f'Был задан следующий вопрос: "{question}". '
                    f'Выпали следующие карты: {user_cards}'
                )
            }
        ]
    )
    return user_cards, completion.choices[0].message.content

    # for index, card in enumerate(cards_for_layout):
    #     position = card.position
    #     user_cards.update({'card': card, 'position': position})
    #
    # return user_cards
