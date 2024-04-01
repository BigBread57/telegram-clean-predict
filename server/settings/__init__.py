"""
This is a django-split-settings main file.

For more information read this:
https://github.com/sobolevn/django-split-settings
https://sobolevn.me/2017/04/managing-djangos-settings

To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

import django_stubs_ext
from split_settings.tools import include

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

_base_settings = (
    'components/common.py',
    'components/logging.py',
    'components/sentry.py',
    'components/csp.py',
    'components/cors.py',
    'components/email.py',
    'components/celery.py',
    'components/telegram.py',
    'components/telethon.py',
    'components/telegram_clean_prediction.py',
    'components/telegram_pay.py',
)

# Include settings:
include(*_base_settings)
