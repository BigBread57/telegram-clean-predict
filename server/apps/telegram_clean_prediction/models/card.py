import random

from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractModel
from server.apps.telegram_clean_prediction.services.enum import (
    DeckType,
    GroupType,
    SuitType,
)


class Card(AbstractModel):
    """Карта."""

    index = models.SmallIntegerField(
        verbose_name=_('Порядковый номер в колоде'),
    )
    group_type = models.CharField(
        verbose_name=_('Тип группы'),
        choices=GroupType.choices,
        max_length=50,
    )
    suit_type = models.CharField(
        verbose_name=_('Тип масти'),
        choices=SuitType.choices,
        max_length=50,
        blank=True,
    )
    image = models.CharField(
        verbose_name=_('Изображение'),
    )
    name = models.CharField(
        verbose_name=_('Название'),
    )
    description = models.JSONField(
        verbose_name=_('Описание'),
    )
    deck_type = models.CharField(
        verbose_name=_('Тип колоды'),
        choices=DeckType.choices,
        max_length=50,
    )

    class Meta(AbstractModel.Meta):
        verbose_name = _('Карта')
        verbose_name_plural = _('Карты')

    def __str__(self):
        return self.name

    @property
    def position(self):
        """Полное имя сотрудника если он прикреплен или пользователя."""
        return random.choices(['inverted', 'straight'], weights=[2, 8])[0]
