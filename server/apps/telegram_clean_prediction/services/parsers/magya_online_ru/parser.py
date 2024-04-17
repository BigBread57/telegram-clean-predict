import requests
from bs4 import BeautifulSoup

from server.apps.telegram_clean_prediction.services.parsers.magya_online_ru.urls import (
    MAJOR_ARCANA,
    TYPE_LAYOUT,
)

SEARCH_PATTERN = {
    'znachenie_kart_taro_v_lyubvi_i_otnosheniyax': {
        'straight': 'значение карты «{card_name}» в любви в прямом положении',
        'inverted': 'перевернутая «{card_name}»: значение в любви и отношениях',
    },

}

def parser_card_info(
    type_layout: str,
    card_data_json: dict,
    card_info: tuple,
    soup: BeautifulSoup,
):
    """Парсинг страницы "Карта в отношениях и любви"."""
    # Переменная для получения информации между заголовками.
    valid_information_for_card = ''
    # Ищем все заголовки.
    for card_information in soup.findAll('h2'):
        # Информация из заголовка.
        card_information_string = card_information.string.lower()
        # Получаем паттерны поиска.
        for type_position, search_pattern in SEARCH_PATTERN.get(type_layout).items():
            # Ищем соответствует ли информация из заголовка, той что нам нужна.
            search_pattern = search_pattern.format(card_name=card_info[1])
            if card_information_string.find(search_pattern) >= 0:
                for sibling in card_information.next_siblings:
                    if sibling.name == 'blockquote':
                        continue
                    if sibling.name == 'h2':
                        break
                    valid_information_for_card = valid_information_for_card + sibling.text

            if not valid_information_for_card:
                continue

            valid_information_for_card = valid_information_for_card.replace('\t\t', ' ')
            valid_information_for_card = valid_information_for_card.replace('\r\n\t', ' ')
            valid_information_for_card = valid_information_for_card.replace('\r', '')
            valid_information_for_card = valid_information_for_card.replace('\t', '')
            valid_information_for_card = valid_information_for_card.replace('\n', '')

            if card_data_json.get(card_info[0]):
                if card_data_json.get(card_info[0]).get(type_layout):
                    card_data_json.get(card_info[0]).get(type_layout).update(
                        {type_position: valid_information_for_card}
                    )
                else:
                    card_data_json.get(card_info[0]).update(
                        {type_layout: {type_position: valid_information_for_card}}
                    )
            else:
                card_data_json.update(
                    {card_info[0]: {type_layout: {type_position: valid_information_for_card}}}
                )

            valid_information_for_card = ''

    return card_data_json


card_data_json = {}
for type_layout in TYPE_LAYOUT:
    for card_info in MAJOR_ARCANA:
        response = requests.get(
            f'https://magya-online.ru/{type_layout}/{card_info[0]}/',
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        parser_card_info(
            type_layout=type_layout,
            card_data_json=card_data_json,
            card_info=card_info,
            soup=soup,
        )
        print(f'Обработана карта {card_info[0]}')
