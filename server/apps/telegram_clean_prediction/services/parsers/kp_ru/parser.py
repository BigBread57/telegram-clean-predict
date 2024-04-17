import time

import requests
from bs4 import BeautifulSoup

from server.apps.telegram_clean_prediction.models import Card
from server.apps.telegram_clean_prediction.services.enum import DeckType
from server.apps.telegram_clean_prediction.services.parsers.kp_ru.urls import (
    ALL_CARDS,
)

SEARCH_PATTERN = {
    ('Положение карты ', 'general_meaning'),
    (' на отношения и любовь', 'love_and_relationships'),
    (' на работу и карьеру', 'work_and_career'),
    (' на финансы', 'finance'),
    (' на здоровье', 'health'),
    (' на ситуацию и вопрос', 'situation_and_question'),
    ('Карта дня: ', 'cards_of_the_day'),
    ('Совет: ', 'advice_card'),
}


def parser_card_info(
    soup: BeautifulSoup,
):
    """Парсинг страницы "Карта в отношениях и любви"."""
    card_data_json = {}
    # Переменная для получения информации между заголовками.
    valid_info_for_card = ''
    type_position = ''
    # Ищем все заголовки.
    for card_information in soup.find_all('h2'):
        # Информация из заголовка.
        for type_layout in SEARCH_PATTERN:
            if card_information.text.find(type_layout[0]) >= 0:
                for sibling in card_information.next_siblings:
                    if sibling.name == 'h2':
                        break
                    if sibling.name in {'div', 'figure', 'script'}:
                        continue
                    if sibling.text == 'Прямое положение':
                        type_position = 'straight'
                    if sibling.text == 'Перевернутое положение':

                        if card_data_json.get(type_layout[1]):
                            valid_info_for_card = valid_info_for_card.replace('\xa0', '')
                            valid_info_for_card = valid_info_for_card.replace(' ', '')
                            valid_info_for_card = valid_info_for_card.replace('\n\n', '')
                            card_data_json.get(type_layout[1]).update(
                                {type_position: valid_info_for_card}
                            )
                        else:
                            valid_info_for_card = valid_info_for_card.replace(
                                '\xa0', '')
                            valid_info_for_card = valid_info_for_card.replace(
                                ' ', '')
                            valid_info_for_card = valid_info_for_card.replace('\n\n', '')
                            card_data_json.update(
                                {type_layout[1]: {
                                    type_position: valid_info_for_card}}
                            )
                        type_position = 'inverted'
                        valid_info_for_card = ''

                    if type_position == '':
                        continue


                    valid_info_for_card = valid_info_for_card + sibling.text


                if card_data_json.get(type_layout[1]):
                    valid_info_for_card = valid_info_for_card.replace('\xa0',
                                                                      '')
                    valid_info_for_card = valid_info_for_card.replace(' ', '')
                    valid_info_for_card = valid_info_for_card.replace('\n\n', '')
                    card_data_json.get(type_layout[1]).update(
                        {type_position: valid_info_for_card}
                    )
                else:
                    valid_info_for_card = valid_info_for_card.replace('\xa0',
                                                                      '')
                    valid_info_for_card = valid_info_for_card.replace(' ', '')
                    valid_info_for_card = valid_info_for_card.replace('\n\n', '')
                    card_data_json.update(
                        {type_layout[1]: {type_position: valid_info_for_card}}
                    )

                type_position = ''
                valid_info_for_card = ''
                break

    return card_data_json


def create_card():
    card_data_obj = []
    for group_type, group_data in ALL_CARDS.items():
        for suit_type, card_info in group_data.items():
            for card in card_info:
                response = requests.get(
                    f'https://www.kp.ru/woman/goroskop/{card["external_name"]}/',
                )
                if response.status_code == 200:
                    print('ok')
                else:
                    print('error')
                soup = BeautifulSoup(response.text, 'html.parser')
                description = parser_card_info(soup=soup)
                card_data_obj.append(
                    Card(
                        index=card['index'],
                        group_type=group_type,
                        suit_type='' if suit_type == 'no_suit_type' else suit_type,
                        image=card['image'],
                        name=card['name'],
                        description=description,
                        deck_type=DeckType.RIDER_WAITE_TAROT,
                    )
                )
                if description:
                    print('ok')
                else:
                    print('error')
                print(f'Обработана карта {card["external_name"]}')
                time.sleep(1)

    Card.objects.bulk_create(card_data_obj)
