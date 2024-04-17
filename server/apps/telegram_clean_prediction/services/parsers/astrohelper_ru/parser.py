import time

import requests
from bs4 import BeautifulSoup

from server.apps.telegram_clean_prediction.models import Card
from server.apps.telegram_clean_prediction.services.enum import DeckType
from server.apps.telegram_clean_prediction.services.parsers.astrohelper_ru.urls import (
    ALL_CARDS,
)

SEARCH_PATTERN = {
    ('общее значение', 'general_meaning'),
    ('значение в любви и отношениях', 'love_and_relationships'),
    ('значение в ситуации и вопросе', 'situation_and_question'),
    ('значение карты дня', 'cards_of_the_day'),
    ('совет карты', 'advice_card'),
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
        card_information_text = card_information.text.lower()
        for type_layout in SEARCH_PATTERN:
            if card_information_text.find(type_layout[0]) >= 0:
                for sibling in card_information.next_siblings:
                    if sibling.name == 'h2':
                        break
                    if sibling.text == 'Прямое положение':
                        type_position = 'straight'
                    if sibling.text == 'Перевернутое положение':

                        if card_data_json.get(type_layout[1]):
                            card_data_json.get(type_layout[1]).update(
                                {type_position: valid_info_for_card}
                            )
                        else:
                            card_data_json.update(
                                {type_layout[1]: {
                                    type_position: valid_info_for_card}}
                            )
                        type_position = 'inverted'
                        valid_info_for_card = ''

                    valid_info_for_card = valid_info_for_card + sibling.text

                if card_data_json.get(type_layout[1]):
                    card_data_json.get(type_layout[1]).update(
                        {type_position: valid_info_for_card}
                    )
                else:
                    card_data_json.update(
                        {type_layout[1]: {type_position: valid_info_for_card}}
                    )

                type_position = ''
                valid_info_for_card = ''
                break

    return card_data_json


def create_card():
    card_data_obj = []
    cookies = {
        'cf_chl_3': '2b4be33107aafdf',
        'cf_clearance': 'hCQf7z1UCdOd7FJWGyr9gVQJ11y._fDjrhDWEZ.1awY-1712247412-1.0.1.1-wRlakOOmTXiulsS783lqUJv_gIf_bcwJgmb9Kz3CB9rrSE65DDRRCz8PFGKvON2JQdeMELu8e5xcPNgT6whX.g',
        'fusionaDul7_visited': 'yes',
        'fusionaDul7_lastvisit': '1712243816',
        '_ym_uid': '1712247417167748091',
        '_ym_d': '1712247417',
        '_ym_isad': '1',
        '_ym_visorc': 'w',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'cf_chl_3=2b4be33107aafdf; cf_clearance=hCQf7z1UCdOd7FJWGyr9gVQJ11y._fDjrhDWEZ.1awY-1712247412-1.0.1.1-wRlakOOmTXiulsS783lqUJv_gIf_bcwJgmb9Kz3CB9rrSE65DDRRCz8PFGKvON2JQdeMELu8e5xcPNgT6whX.g; fusionaDul7_visited=yes; fusionaDul7_lastvisit=1712243816; _ym_uid=1712247417167748091; _ym_d=1712247417; _ym_isad=1; _ym_visorc=w',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"123.0.6312.60"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.60", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.60"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    for group_type, group_data in ALL_CARDS.items():
        for suit_type, card_info in group_data.items():
            for card in card_info:
                headers.update(
                    {
                        'referer': f'https://astrohelper.ru/gadaniya/taro/znachenie/{card["external_name"]}',
                    }
                )
                response = requests.get(
                    f'https://astrohelper.ru/gadaniya/taro/znachenie/{card["external_name"]}/',
                    cookies=cookies,
                    headers=headers,
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
                time.sleep(2)

    Card.objects.bulk_create(card_data_obj)
