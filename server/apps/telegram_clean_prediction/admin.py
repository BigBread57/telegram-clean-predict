import json

from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets

from server.apps.telegram_clean_prediction.models import (
    Card,
    Client,
    Layout,
    LayoutCards,
)


class CustomJSONWidget(widgets.Textarea):
    """Виджет для json поля."""

    def format_value(self, value):
        """Формат вывода json поля."""
        try:
            value = json.dumps(
                json.loads(value),
                indent=4,
                sort_keys=True,
                ensure_ascii=False,
            )
            # Эти строки попытаются настроить размер TextArea в соответствии
            # с содержимым.
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception:
            return super(CustomJSONWidget, self).format_value(value)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """Админка для Card."""

    list_display = (
        'id',
        'index',
        'name',
    )
    ordering = (
        '-id',
    )
    formfield_overrides = {
        JSONField: {'widget': CustomJSONWidget}
    }


admin.site.register(Client)
admin.site.register(Layout)
admin.site.register(LayoutCards)
