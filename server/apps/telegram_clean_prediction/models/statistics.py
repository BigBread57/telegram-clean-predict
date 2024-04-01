from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel


class Statistics(AbstractModel):
    """Статистика клиента."""

    client = models.OneToOneField(
        to='telegram_clean_prediction.Client',
        verbose_name=_('Клиент'),
        on_delete=models.CASCADE,
        related_name='statistics',
    )
    successfully_listened = models.SmallIntegerField(
        verbose_name=_(
            'Количество клиентов, которые были довольны тем, что их выслушали',
        ),
        default=0,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Статистика клиента')
        verbose_name_plural = _('Статистика клиентов')

    def __str__(self):
        return f'{self.client}'