from server.settings.components import config

TELETHON_API_ID = config(
    'TELETHON_API_ID',
    cast=int,
    default=0,
)

TELETHON_API_HASH = config(
    'TELETHON_API_HASH',
    cast=str,
    default='',
)

TELETHON_PHONE = config(
    'TELETHON_PHONE',
    cast=str,
    default='',
)
