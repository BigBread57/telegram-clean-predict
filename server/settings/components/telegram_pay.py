"""Настройки для создаваемой app."""
from server.settings.components import config

MAX_STRING_LENGTH = 255

TELEGRAM_PROVIDER_TOKEN_YKASSA = config(
    'TELEGRAM_PROVIDER_TOKEN_YKASSA',
    cast=str,
    default='',
)

YKASSA_SHOP_ID = config(
    'YKASSA_SHOP_ID',
    cast=int,
    default=506751,
)

YKASSA_SHOP_ARTICLE_ID = config(
    'YKASSA_SHOP_ARTICLE_ID',
    cast=int,
    default=538350,
)
