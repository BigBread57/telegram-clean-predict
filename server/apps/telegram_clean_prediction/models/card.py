from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel


class Card(AbstractModel):
    """Карта"""

    image = models.CharField(
        verbose_name=_('Изображение'),
    )
    name = models.CharField(
        verbose_name=_('Название'),
        blank=True,
    )
    description = models.JSONField(
        verbose_name=_('Описание'),
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Карта')
        verbose_name_plural = _('Карты')

    def __str__(self):
        return self.name
