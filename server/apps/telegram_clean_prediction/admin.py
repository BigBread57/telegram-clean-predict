from django.contrib import admin

from server.apps.telegram_clean_prediction.models import (
    Client,
    Statistics,
)

admin.site.register(Client)
admin.site.register(Statistics)
