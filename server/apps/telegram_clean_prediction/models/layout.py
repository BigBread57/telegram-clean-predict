from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel


class Layout(AbstractModel):
    """Расклад Таро."""

    client = models.IntegerField(
        verbose_name=_('Клиент'),
    )
    type_layout = models.CharField(
        verbose_name=_('Тип расклада'),
    )
    cards = models.ManyToManyField(

    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Статистика клиента')
        verbose_name_plural = _('Статистика клиентов')

    def __str__(self):
        return f'{self.client}'